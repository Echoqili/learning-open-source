---
name: "superpowers-openspec-pipeline"
description: "把 Superpowers 的脑暴/TDD 能力与 OpenSpec(speckit) 的 change 工作流串成一条自动化 Skill：explore → propose（风险分级+人工审核）→ apply（TDD）→ 工具化 redline-check → 人工验收 → archive。支持 Gherkin 可执行规格、模块化 spec 基线、AI 变更追踪。"
license: MIT
compatibility: "纯 Prompt 驱动，需配合 OpenSpec change 工作流使用；产物统一收敛到 openspec/changes/{change_name}/。"
metadata:
  version: "3.2.0"
  author: "自定义总控串联 Skill"
---

# Superpowers + OpenSpec(speckit) 总控串联 Skill

## 触发条件

用户表达以下任一意图时激活：

- “用 Superpowers + OpenSpec 跑一遍”
- “启动 change 流水线”
- “帮我走 /opsx:explore → /opsx:propose → /opsx:apply → archive”
- 输入原始业务需求并准备进入完整开发流水线
- 显式指定模式：
  - **思考模式**（默认）：无特殊关键词，或出现“完整走一遍”、“深度模式”、“认真设计”
  - **省 token 模式**：出现“快速模式”、“极速模式”、“省 token”、“简单做”、“fast mode”、“原型”

## 设计目标

1. 把 AI 的“发散能力”锁死在规范阶段，编码阶段只能按图施工。
2. 用风险分级决定门禁强度：低风险快、高风险严。
3. 把验收标准写成 Gherkin 可执行规格，让测试用例直接对应业务行为。
4. redline-check 优先调用真实扫描工具，LLM 自检只做兜底。
5. 通过 archive 把每次 change 的约束沉淀到模块化 spec 基线，长期抑制 AI 漂移。
6. 自动记录 AI 变更元数据，方便后续追溯、度量和审计。
7. 用风险分级、增量更新、必要才生成等手段控制 token 消耗，避免约束过度膨胀。

## 运行模式

本 Skill 提供两种互斥模式，由用户在触发时指定；未指定时默认进入**思考模式**。

### 1. 思考模式（think，默认）

- **目标**：追求需求完整、方案清晰、长期可维护，适合核心功能、高风险模块、需要沉淀规范的项目。
- **行为特征**：
  - 需求模糊时执行 `/opsx:explore`。
  - `/opsx:propose` 生成完整 `proposal.md` + `design.md` + `tasks.md` + `features/*.feature` + `specs/` 增量。
  - 中/高风险必须走关卡①人工审核。
  - `/opsx:apply` 每个 task 详细报告 Red/Green/Refactor 状态。
  - `/redline-check` 完整扫描 + LLM 上下文审计。
  - 关卡④逐项对照 `proposal.md` / `features/*.feature` 验收。
  - `/opsx:archive` 合并到对应领域 spec 基线。

### 2. 省 token 模式（fast）

- **目标**：最小 token 消耗、最快交付，适合原型、内部工具、低风险小功能、快速验证想法。
- **触发词**：“快速模式”、“极速模式”、“省 token”、“简单做”、“fast mode”、“原型”。
- **行为特征**：
  - 默认跳过 `/opsx:explore`，除非用户明确说需求模糊。
  - `/opsx:propose` 只生成 `proposal.md` + `tasks.md`；`design.md` 极简（仅关键技术选型与接口契约）；不生成 `features/*.feature` 和 `specs/` 增量。
  - 未显式要求时默认按 **low 风险**处理，跳过关卡①。
  - `/opsx:apply` 每批 task 聚合汇报，只展示失败详情，通过项一句话带过。
  - `/redline-check` 只跑 lint + 单元测试；LLM 自检仅对失败项做快速摘要。
  - 关卡④简化为“功能是否符合需求？”一问。
  - `/opsx:archive` 只更新 `META.md`，不立即合并全局 spec 基线；用户确认后再合并或留待后续批量归档。

### 3. 模式切换规则

- 若用户未指定模式，按思考模式执行。
- 若用户在同一次对话中切换模式（例如“刚才快速模式，现在重新深度设计”），重新从 `/opsx:propose` 开始。
- 模式信息写入 `META.md` 的 `mode` 字段，便于后续追溯。

## 省 token 与流畅性原则

约束越多，单次 Prompt 越长、多轮对话越多，token 消耗必然上升。本 Skill 通过以下设计把额外开销压到最小：

1. **风险分级裁剪流程**  
   低风险 change 跳过关卡①，redline 只跑 lint + 测试；只有高风险才走完整人工审核和 SAST。

2. **明确需求时跳过 explore**  
   用户一次把验收标准、范围、约束说清楚，直接进 `/opsx:propose`，省掉一轮脑暴。

3. **产物按需生成**  
   Gherkin feature、specs 增量、安全复核报告只在需要时生成，不默认全量输出。

4. **阶段内使用摘要而非全文回传**  
   `/opsx:apply` 每完成一个 task 只报告“任务 ID + 文件 + 测试结果摘要”，不重复贴出整份 `tasks.md`。

5. **增量修改而非重写**  
   需求中途变更时，只更新被改动的规范段落，不重新生成整份 `proposal.md` / `tasks.md`。

6. **工具化 redline 替代 LLM 长自检**  
   配置 `redline.yml` 让外部命令做扫描，LLM 只解析命令输出，比让 LLM 逐行读代码省大量 token。

7. **低优先级信息折叠**  
   详细的设计方案、依赖图、完整 redline 原始日志默认不显示，仅在有错误时才展开。

8. **短期缓存避免重复读取**  
   同一轮对话中已读取的规范文档、feature 文件缓存到上下文，不反复从磁盘读取。

9. **双模式按需切换**  
   默认思考模式保证质量，用户说“快速模式/极速模式/省 token/简单做/fast mode/原型”时自动进入省 token 模式，走最短路径。

## 执行总序

```text
原始需求输入
    │
    ├─ 需求模糊？ ──是──> /opsx:explore（Superpowers 脑暴，不写文件）
    │                       │
    │                       否 或 脑暴完成
    │                       ▼
    │            /opsx:propose（生成 change 规范文档 + 风险分级）
    │                       │
    │            人工审核关卡①（低风险可跳过，中/高风险必须 approve）
    │                       ▼
    │            /opsx:apply（强制 TDD 模式执行 tasks）
    │                       │
    │            编译/测试门禁关卡②（自动运行，失败拦截）
    │                       ▼
    │            /redline-check（按风险级别调用工具化扫描）关卡③
    │                       │
    │            存在阻断项？ ──是──> 修复后重新 redline-check
    │                       否
    │                       ▼
    │            人工功能验收关卡④（必须显式 approve）
    │                       ▼
    │            /opsx:archive（合并到对应领域 spec 基线 + 生成元数据）
    │                       ▼
    │            输出总结报告
```

## 产物目录规范

```text
openspec/
├── config/
│   └── redline.yml                  # redline 扫描命令配置（可选，首次生成）
├── specs/
│   └── <domain>.md                  # 按领域拆分的全局 spec 基线（archive 后更新）
└── changes/
    └── {change_name}/
        ├── META.md                  # change 元数据（风险等级、AI 生成标记、影响域）
        ├── proposal.md              # 需求提案
        ├── design.md                # 设计方案
        ├── tasks.md                 # 任务拆分
        ├── specs/                   # 对全局 spec 的增量/变更（可选）
        │   └── <domain>.md
        └── features/                # Gherkin 可执行规格（可选，推荐生成）
            └── {change_name}.feature
```

---

## 阶段一：需求澄清 — `/opsx:explore`

当需求模糊、边界不清或缺少验收标准时执行；需求已明确则跳过。

1. 调用 Superpowers brainstorm 能力（以 `/opsx:explore` 形式执行）。
2. 主动澄清不清晰点，输出结构化 BrainstormDraft。
3. 草稿仅保存在当前对话上下文/内存变量中，**不写任何本地文件**。
4. 草稿至少包含：业务目标、用户场景、2 个以上候选方案、推荐方案及理由、风险与依赖、待确认问题。

---

## 阶段二：生成规范 — `/opsx:propose`

### 2.1 change 命名

1. 自动按 `YYYYMMDD-<short-kebab-feature>` 生成 change_name，例如 `20260623-order-list-status-filter`。
2. 若用户已指定名称，直接使用；若名称冲突，提示用户调整。
3. 创建目录 `openspec/changes/{change_name}/`。

### 2.2 风险分级

生成规范的同时，根据以下维度自动判定风险等级，并询问用户确认：

| 等级 | 判定条件 | 门禁策略 |
|------|----------|----------|
| low | 纯新增功能、不涉及敏感数据/权限/公共 API/性能瓶颈 | 跳过关卡①；redline 走轻量扫描 |
| medium | 普通业务功能，涉及用户数据或内部 API | 默认流程：关卡① + 标准 redline |
| high | 涉及权限/支付/安全/公共 API/数据迁移/跨服务/性能核心路径 | 关卡① + 额外安全复核 + 完整 redline |

用户可显式覆盖分级，例如“按高风险处理”。

### 2.3 生成文档

在该目录下生成：

- `META.md`：change 元数据（含 `mode`）
- `proposal.md`：需求提案
- `design.md`：设计方案
- `tasks.md`：任务拆分
- `specs/`（可选）：对全局 spec 的增量/修改
- `features/`（可选但推荐）：Gherkin 可执行规格

**按模式裁剪**：

- 思考模式：全部生成。
- 省 token 模式：只生成 `proposal.md` + `tasks.md`；`design.md` 极简（≤ 20 行，只留技术选型与接口契约）；不生成 `specs/` 和 `features/`。

### 2.4 META.md 模板

```markdown
# Change: {change_name}

- status: proposed
- created_at: YYYY-MM-DD
- mode: think | fast
- risk_level: low | medium | high
- ai_generated: true
- domain: <领域，如 order/user/payment>
- affected_files: []
- summary: <一句话描述>
```

### 2.5 proposal.md 模板

```markdown
# Proposal: <功能标题>

## 1. 背景与目标
- 业务背景：...
- 功能目标：...
- 成功指标：...

## 2. 用户故事 / 验收标准
| 编号 | 用户故事 | 验收标准（可验证） |
|------|----------|-------------------|
| AC-1 | 作为...，我希望...，以便... | 当...时，期望... |

## 3. 范围
### In Scope
- ...
### Out of Scope
- ...

## 4. 功能需求
- FR-1: ...
- FR-2: ...

## 5. 非功能需求
- 性能：...
- 安全：...
- 可维护性：...

## 6. 约束与假设
- ...

## 7. 验收清单
- [ ] AC-1 已实现并通过测试
- [ ] AC-2 已实现并通过测试
- [ ] ...
```

### 2.6 design.md 模板

```markdown
# Design: <功能标题>

## 1. 架构概览
- 模块关系图（文字描述或 Mermaid）
- 数据流向

## 2. 技术选型
| 层级 | 选型 | 理由 |
|------|------|------|
| 语言/框架 | ... | ... |
| 测试框架 | ... | ... |
| 构建/部署 | ... | ... |

## 3. 模块划分
| 模块 | 职责 | 关键接口/文件 |
|------|------|--------------|
| ... | ... | ... |

## 4. 数据模型 / API 契约
- 实体定义
- 请求/响应格式
- 错误码约定

## 5. 错误处理与日志
- ...

## 6. 测试策略
- 单元测试覆盖率目标
- 集成测试范围
- Mock 策略

## 7. 风险与降级方案
| 风险 | 影响 | 应对措施 |
|------|------|----------|
| ... | ... | ... |
```

### 2.7 tasks.md 模板

```markdown
# Tasks: <功能标题>

> 本表由 `/opsx:propose` 生成，编码阶段仅作为执行蓝图，**不得修改本文档内容**。

| ID | 优先级 | 依赖 | 任务描述 | 验收标准 | 估算 |
|----|--------|------|----------|----------|------|
| T1 | P0 | - | 搭建项目骨架与依赖 | 项目可编译/运行 | ... |
| T2 | P0 | T1 | 编写 XX 的单元测试（Red） | 测试运行且失败 | ... |
| T3 | P0 | T2 | 实现 XX 通过测试（Green） | 测试通过 | ... |
| ... | ... | ... | ... | ... | ... |

## 依赖图
```text
T1 -> T2 -> T3 -> ...
```
```

### 2.8 Gherkin 可执行规格（推荐生成）

把 `proposal.md` 中的验收标准转写成 `features/{change_name}.feature`：

```gherkin
Feature: <功能标题>

  Background:
    Given <前置条件>

  Scenario: AC-1 <简短描述>
    Given <上下文>
    When <动作>
    Then <期望结果>

  Scenario: AC-2 <简短描述>
    ...
```

如果项目已接入 Cucumber、Behave、SpecFlow 等框架，这些 scenarios 可直接绑定到自动化测试；未接入时，它们作为活文档与单元测试一一对应。

### 2.9 人工审核关卡①

- **low 风险**：默认跳过本关卡，直接告诉用户“已按低风险进入 apply，如需审核可回复‘暂停’”。
- **medium / high 风险**：主动停止并请求用户审核。仅当用户明确回复“通过” / “approve” / “ok” / “继续” / “进入 apply” 时，方可继续。

若用户提出修改意见，按意见更新 `proposal.md` / `design.md` / `tasks.md` / `specs/` / `features/`，更新后再次请求审核，直至通过。

---

## 阶段三：受控实现 — `/opsx:apply`

用户通过关卡①（或被低风险跳过）后，以 Superpowers TDD 能力执行。

### 3.1 前置读取

1. 读取 `openspec/changes/{change_name}/` 下全部规范文档。
2. 在内存中按依赖顺序建立任务队列。
3. 读取 `features/*.feature` 作为验收测试的输入。

### 3.2 每个任务的 TDD 循环

对每个任务：

1. **Red**：先写测试用例，运行并确认失败。
2. **Green**：编写最少量业务代码使测试通过。
3. **Run**：运行对应测试/编译；失败时只改代码/测试，不修改 changes 目录下任何规范文档。
4. **Refactor**：在测试通过前提下重构，保持行为不变。

### 3.3 对现有代码的改动

本阶段以新增为主。若必须修改既有代码（例如最小范围适配接口），允许改动，但须满足：

- 改动范围最小，且不引入新行为；
- 在报告中说明改动的文件与原因；
- 仍禁止修改 changes 目录下的规范文档。

### 3.4 硬性约束

- 仅新增代码文件、测试文件、测试用例、配置文件、依赖声明。
- 禁止修改 `openspec/changes/{change_name}/` 下的 `META.md`、`proposal.md`、`design.md`、`tasks.md`、`specs/`、`features/` 中的已有内容。
- 禁止实现未在 `proposal.md` 验收标准或 `features/*.feature` 中列出的功能。
- 技术选型、模块划分、接口契约遵循 `design.md`。
- 每个 task 至少对应一个可运行的测试用例。
- 测试框架与语言遵循 `design.md`。

### 3.5 完成报告

- 思考模式：每完成一个任务报告任务 ID、新增/修改的代码与测试文件、测试结果摘要。
- 省 token 模式：每批任务聚合汇报，只列出失败的文件与修复建议，通过的用一句话总结，例如“T1-T4 全部通过，新增 3 个文件、2 个测试”。

---

## 阶段四：红线自检 — `/redline-check`

全部 tasks 完成后执行。优先读取并调用 `openspec/config/redline.yml` 中配置的命令；未配置时，再用 LLM 自检兜底。

### 4.1 redline 配置示例

首次执行 `/redline-check` 且配置不存在时，可提示用户创建 `openspec/config/redline.yml`：

```yaml
# openspec/config/redline.yml
low:
  - name: lint
    cmd: npm run lint
    block_on_failure: true
  - name: unit-test
    cmd: npm test -- --run
    block_on_failure: true

medium:
  - name: lint
    cmd: npm run lint
    block_on_failure: true
  - name: unit-test
    cmd: npm test -- --run
    block_on_failure: true
  - name: secret-scan
    cmd: gitleaks detect --source .
    block_on_failure: true
  - name: type-check
    cmd: npm run typecheck
    block_on_failure: true

high:
  - name: lint
    cmd: npm run lint
    block_on_failure: true
  - name: unit-test
    cmd: npm test -- --run
    block_on_failure: true
  - name: secret-scan
    cmd: gitleaks detect --source .
    block_on_failure: true
  - name: type-check
    cmd: npm run typecheck
    block_on_failure: true
  - name: sast
    cmd: sonar-scanner
    block_on_failure: true
  - name: dependency-audit
    cmd: npm audit --audit-level=high
    block_on_failure: true
```

### 4.2 执行规则

1. 按风险等级选择对应命令列表。
2. 顺序执行每条命令；失败时立即停止，报告命令输出、失败文件、修复建议。
3. 所有命令通过后：
   - 思考模式：再用 LLM 做补充上下文审计（如权限边界、业务逻辑漏洞）。
   - 省 token 模式：跳过 LLM 审计，或仅对失败命令输出做快速摘要。
4. 发现阻断项：修复后重新 `/redline-check`。
5. 仅存在建议项：可继续，但在总结中列出。

**省 token 模式额外简化**：

- 只执行 `low` 级别的命令（lint + 单元测试），不执行 secret-scan / SAST / 依赖审计。

### 4.3 无配置时的 LLM 兜底扫描范围

| 红线项 | 检查内容 |
|--------|----------|
| 多租户隔离 | 查询是否带 tenant 过滤，跨租户数据访问是否被拦截 |
| 入参 DTO/校验 | 是否使用强类型 DTO/Request 对象，是否校验必填/格式/范围 |
| SQL 注入/N+1 | 是否存在 SQL 注入风险、N+1 查询、慢查询 |
| 权限/auth | 接口是否鉴权，敏感操作是否有权限校验 |
| 敏感信息泄露 | 是否硬编码密钥、token、密码 |
| 异常/错误处理 | 是否捕获并规范化异常，是否泄露内部堆栈 |
| 日志脱敏 | 是否记录关键操作，是否避免打印敏感字段 |
| 并发/幂等 | 关键操作是否考虑并发、幂等、分布式锁 |

---

## 阶段五：人工功能验收关卡④

红线通过后请求用户验收：

- 思考模式：用户对照 `proposal.md` 和 `features/*.feature` 的验收标准逐项验证。仅当用户明确回复“通过” / “approve” / “ok” / “归档” 时，方可执行 `/opsx:archive`。
- 省 token 模式：只问一句“功能是否符合需求？”；用户确认“是/通过/ok”即可归档。
- 验收不通过时，回到 `/opsx:apply` 或 `/redline-check` 循环修复，直到通过。

---

## 阶段六：归档闭环 — `/opsx:archive`

验收通过后执行：

### 思考模式

1. 确定本次 change 所属领域 `domain`（来自 `META.md`）。
2. 将 `openspec/changes/{change_name}/specs/<domain>.md` 的增量/变更合并进 `openspec/specs/<domain>.md` 基线；若不存在则新建。
3. 更新 `META.md` 的 `status` 为 `archived`，并补充 `archived_at` 和 `affected_files`。
4. 输出最终总结报告，包含建议的 commit message：
   ```text
   [ai-generated] change(20260623-order-list-status-filter): <一句话描述>
   
   - 对应 proposal: openspec/changes/20260623-order-list-status-filter/proposal.md
   - 影响领域: order
   ```

### 省 token 模式

1. 更新 `META.md` 的 `status` 为 `archived`，补充 `archived_at` 和 `affected_files`。
2. **不自动合并**全局 spec 基线；在总结中提示用户：
   - “如需沉淀规范，请回复‘合并到领域 spec’。”
   - 或批量处理：多个 fast change 完成后，统一由用户决定哪些需要归档到 `openspec/specs/<domain>.md`。
3. 输出极简总结：change 名称、新增文件数、测试通过数、建议 commit message。

---

## 阶段七：异常终止 — `/opsx:abort`

如果用户在任意阶段决定放弃本次 change：

1. 停止当前执行。
2. 更新 `META.md` 的 `status` 为 `aborted`，并记录原因。
3. 不执行 `/opsx:archive`，不更新全局 spec 基线。
4. 提示用户是否回滚已生成的代码/测试文件（由用户决定，不自动删除）。

---

## 需求中途变更的处理

若在 `/opsx:apply` 或验收阶段发现需求必须调整：

1. 暂停当前阶段，不直接修改 changes 目录下的规范文档。
2. 回到 `/opsx:propose`，按新需求重新生成或更新规范文档。
3. 重新通过对应风险等级的关卡①后，再进入 `/opsx:apply`。

---

## 与 CI / 版本控制的边界

本 Skill 运行在 IDE 层，是开发辅助流程，不替代团队既有的 CI/CD、代码审查、分支策略。生成的代码仍应通过：

- 正常的 PR/MR 审查；
- 团队 CI 中的 lint、测试、SAST、DAST、依赖扫描；
- 代码合并与发布流程。

Skill 内的门禁是对个人开发节奏的约束，CI 门禁是对代码入库的约束，二者互补。

---

## 完成定义（Definition of Done）

一次 change 只有在以下全部满足时才算完成：

- [ ] `META.md`、`proposal.md`、`design.md`、`tasks.md`、`specs/`、`features/` 在编码阶段未被修改。
- [ ] 所有 tasks 都有对应测试，且测试全部通过。
- [ ] `/redline-check` 无阻断项。
- [ ] 用户通过关卡④验收。
- [ ] `/opsx:archive` 已执行，对应领域 spec 基线已更新。
- [ ] `META.md` 已标记 `status: archived` 和 `affected_files`。

---

## 反模式

| 反模式 | 正确做法 |
|--------|----------|
| `/opsx:explore` 写出临时方案文档 | 仅保留在内存中 |
| `/opsx:propose` 顺手写代码或测试 | 只写规范文档 |
| 用户未审核就自动进入 `/opsx:apply`（中/高风险） | 必须等待关卡①显式通过 |
| `/opsx:apply` 修改 changes 目录下的规范文档 | 禁止修改，需求变更走重新 propose |
| 红线阻断项仍进入人工验收 | 修复后重新 `/redline-check` |
| 验收未通过就归档 | 必须等待关卡④通过 |
| 不归档、不更新领域 spec | 必须执行 `/opsx:archive` |
| 实现中临时加入未在 proposal/feature 中的功能 | 超出范围，剔除或重新走 propose |

---

## 一键口令示例

### 思考模式（默认）

> “帮我用 Superpowers + OpenSpec 流水线实现：用户登录后能看到自己的订单列表，支持按状态筛选。”

本 Skill 自动执行：

```text
/opsx:explore（如需求模糊）
    ↓
/opsx:propose → 完整 proposal/design/tasks/feature/specs + 风险分级 + （中高风险）人工审核①
    ↓
/opsx:apply（TDD，逐条详细报告） → 编译/测试门禁②
    ↓
/redline-check（完整扫描 + LLM 审计）关卡③
    ↓
人工功能验收④（逐项核对验收标准）
    ↓
/opsx:archive → 合并领域 spec 基线 + 生成 AI 变更元数据
```

### 省 token 模式

> “快速模式：帮我用 Superpowers + OpenSpec 做个订单列表状态筛选，简单做就行。”

本 Skill 自动执行：

```text
跳过 /opsx:explore
    ↓
/opsx:propose → 极简 proposal/tasks + 极简 design（low 风险跳审核）
    ↓
/opsx:apply（TDD，批量聚合报告） → 编译/测试门禁②
    ↓
/redline-check（仅 lint + 单元测试）
    ↓
人工功能验收④（一问确认）
    ↓
/opsx:archive → 更新 META.md，不自动合并全局 spec（可后续批量处理）
```
