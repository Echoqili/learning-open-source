---
name: "superpowers-openspec-pipeline"
description: "把 Superpowers 的脑暴/TDD 能力与 OpenSpec(speckit) 的 change 工作流串成一条自动化 Skill：explore → propose（风险分级+自适应门禁）→ apply（TDD/smoke）→ 工具化 redline-check → 验收 → archive。支持三种模式（思考/省 token/性价比）、自适应门禁（人工/智能校验/跳过）、Gherkin 可执行规格、模块化 spec 基线、AI 变更追踪。"
license: MIT
compatibility: "纯 Prompt 驱动，需配合 OpenSpec change 工作流使用；产物按模式收敛到 openspec/changes/{change_name}/ 或 .cost-upgrader/changes/{change_name}/。"
metadata:
  version: "3.4.0"
  author: "自定义总控串联 Skill"
---

# Superpowers + OpenSpec(speckit) 总控串联 Skill

## 触发条件

本 Skill 只在用户明确表达以下任一**激活词**时启用；普通编码请求不触发，避免默认消耗大量 token：

- “用 Superpowers + OpenSpec”
- “启动 change 流水线”
- “帮我走 /opsx:explore → /opsx:propose → /opsx:apply → archive”
- 提到任一 `/opsx:` 命令

## 模式选择

激活后，必须明确选择模式。**不能默认进入任一模式**，避免边界模糊。按以下关键词判断：

### 思考模式关键词

用户表达中出现任意一个即进入思考模式：

- “思考模式”、“think mode”
- “完整流程”、“规范流程”、“完整走一遍”
- “深度模式”、“认真设计”
- “需要沉淀规范”、“写完整设计”

### 省 token 模式关键词

用户表达中出现任意一个即进入省 token 模式：

- “快速模式”、“极速模式”
- “省 token”、“简单做”
- “fast mode”、“quick mode”
- “原型”、“先跑通”

### 性价比模式关键词

用户表达中出现任意一个即进入性价比模式：

- “省钱做”、“性价比”
- “实用点”、“降本”
- “用最便宜的方式”、“最小可行”
- “简单能跑就行”、“不要写那么多文档”
- “怎么便宜怎么来”

### 智能校验关键词（门禁形态，与模式正交）

用户表达中出现任意一个即进入智能校验门禁：

- “智能校验”、“auto-review”
- “智能复核”、“AI 审核”

**默认行为**：

| 模式 | 默认 `gate_mode` | 关卡①行为 | 能否切换 |
|---|---|---|---|
| 思考模式 | `auto-review` | 中/高风险智能校验，low 风险直接放行 | 可切 `human` |
| 省 token 模式 | `human` | low 风险跳过；中/高风险人工复核 | 可切 `auto-review` |
| 性价比模式 | `skipped` | 始终跳过 | 不可切换 |

- **思考模式**默认开启智能校验门禁；用户可显式说“关闭智能校验 / 走人工”切换为人工门禁。
- **省 token 模式**默认**不开启**智能校验，走“人工 / low 跳过”原逻辑；用户可显式说“智能校验”开启。
- **性价比模式**为压成本，门禁直接 `skipped`，不审核。

**一句话区分**：

- **人工门禁**：必须等用户显式“通过 / approve”才能进入 apply。
- **智能校验门禁**：AI 调用 redline 工具与 LLM 预审产出结构化报告，按风险等级与置信度决定是否升级人工；low 风险下直接进 apply。
- **思考模式**：你要 AI 先写完整需求/设计/验收标准，再编码，适合重要功能。
- **省 token 模式**：你直接让 AI 写代码，只留最简任务列表，适合原型或低风险小改动。
- **性价比模式**：只要最低成本能跑起来，产物极简，适合临时脚本、验证想法、内部小工具。

## 设计目标

1. 把 AI 的“发散能力”锁死在规范阶段，编码阶段只能按图施工。
2. 用风险分级决定门禁强度：低风险快、高风险严。
3. 把验收标准写成 Gherkin 可执行规格，让测试用例直接对应业务行为。
4. redline-check 优先调用真实扫描工具，LLM 自检只做兜底。
5. 通过 archive 把每次 change 的约束沉淀到模块化 spec 基线，长期抑制 AI 漂移。
6. 自动记录 AI 变更元数据，方便后续追溯、度量和审计。
7. 用风险分级、增量更新、必要才生成等手段控制 token 消耗，避免约束过度膨胀。

## 运行模式

本 Skill 提供两种互斥模式，必须由用户在触发时**显式选择**，无默认模式。

### 1. 思考模式（think）

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

### 3. 性价比模式（practical）

- **目标**：用最低成本把模糊需求变成“能跑、能验证、能复用”的交付物，适合临时脚本、验证想法、内部小工具、非核心一次性需求。
- **触发词**：“省钱做”、“性价比”、“实用点”、“降本”、“用最便宜的方式”、“最小可行”、“简单能跑就行”、“不要写那么多文档”、“怎么便宜怎么来”。
- **行为特征**：
  - 默认跳过 `/opsx:explore`，除非需求极模糊。
  - `/opsx:propose` 只生成 `plan.md`（≤ 30 行） + `TASKS.md`（≤ 10 条）；**不生成** `proposal.md` / `design.md` / `features/` / `specs/`。
  - 产物收敛到 `.cost-upgrader/changes/{change_name}/`，与 `openspec/` 解耦。
  - 默认按 **low 风险**处理；跳过关卡①；**不开启**智能校验门禁。
  - `/opsx:apply` 不强制 TDD，优先“写最小代码 → 跑 smoke test → 修到能跑”。
  - `/redline-check` 简化为一次 ≤ 30 秒的 smoke test；失败时最多修 3 轮，仍失败则降级为“手动步骤”继续。
  - 关卡④简化为一句“功能是否符合需求？”（人工回答）或跳过（用户说“不用验收”）。
  - `/opsx:archive` 只更新 `META.md`，并把可复用片段归档到 `.cost-upgrader/snippets/<feature>-<n>.md`；不合并 `openspec/specs/`。
  - 全过程需向用户报告“成本账”：时间、token 估算、新增依赖、文件数。

### 4. 冲突与缺省处理

- **同时出现多类模式关键词**：停止并询问用户“请选择 思考模式 / 省 token 模式 / 性价比模式？”，不猜测。
- **均未出现**：停止并询问：
  ```text
  请选择运行模式：
  1. 思考模式：完整需求/设计/验收标准 + 完整门禁（适合重要功能）
  2. 省 token 模式：最简任务列表 + 轻量门禁（适合原型/小改动）
  3. 性价比模式：最低成本跑起来 + 极简产物（适合临时脚本/验证想法）
  ```
- **模式确定后写入 `META.md` 的 `mode` 字段**，本 change 不再改变。

### 5. 模式切换规则

- 若用户在同一次对话中切换模式（例如“刚才快速模式，现在重新深度设计”），重新从 `/opsx:propose` 开始。
- 切换模式时，已生成的产物按新模式重新裁剪；原产物保留历史版本（文件名加 `.v1` / `.v2` 后缀或移入 `archive/` 子目录），避免丢失上下文。
- **不允许的切换**：性价比模式进行中不可切换到思考/省 token 模式（成本目标冲突）；如需切换，必须废弃当前 change 重新创建。

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

9. **三模式按需切换**  
   思考模式保质量，省 token 模式保速度，性价比模式保成本；用户关键词决定进入哪条路径。

10. **性价比模式专属裁剪**  
    不生成 `proposal.md` / `design.md` / `features/` / `specs/`；产物收敛到 `.cost-upgrader/`；只跑 smoke；不强制 TDD。

## 执行总序

```text
原始需求输入
    │
    ├─ 需求模糊？ ──是──> /opsx:explore（Superpowers 脑暴，不写文件；性价比模式可跳过）
    │                       │
    │                       否 或 脑暴完成
    │                       ▼
    │            /opsx:propose（生成 change 规范文档 + 风险分级 + gate_mode）
    │                       │
    │            ├─ 性价比模式？ ──是──> 产物到 .cost-upgrader/，只生成 plan.md + TASKS.md
    │            │
    │            审核关卡①（性价比模式跳过；其它按 gate_mode 选 ①-A 智能校验 / ①-B 人工）
    │                       ▼
    │            /opsx:apply（思考/省 token 模式强制 TDD；性价比模式先 smoke 后兜底）
    │                       │
    │            编译/测试门禁关卡②（性价比模式简化为 smoke test）
    │                       ▼
    │            /redline-check（按风险级别/模式调用工具化扫描）关卡③
    │                       │
    │            存在阻断项？ ──是──> 修复后重新 redline-check（性价比模式失败 3 轮降级手动）
    │                       否
    │                       ▼
    │            功能验收关卡④（人工/智能校验二选一；性价比模式可跳过）
    │                       ▼
    │            /opsx:archive（思考模式合并 openspec/specs/；性价比模式归档 snippets 到 .cost-upgrader/）
    │                       ▼
    │            输出总结报告（性价比模式附成本账）
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


### 模式速查表

| 维度 | 思考模式 | 省 token 模式 | 性价比模式 |
|---|---|---|---|
| 目标 | 质量、可维护、规范沉淀 | 速度、最小 token | 最低成本、能跑就行 |
| explore | 需求模糊时执行 | 默认跳过 | 默认跳过 |
| 规范产物 | proposal + design + tasks + features + specs | proposal + tasks + 极简 design | plan + TASKS |
| 产物目录 | `openspec/changes/` | `openspec/changes/` | `.cost-upgrader/changes/` |
| 门禁 | 智能校验（默认可切人工） | 人工（默认可切智能校验） | 跳过 |
| TDD | 强制 | 强制 | 不强制，先 smoke |
| redline | 按风险等级完整扫描 | 仅 low 级别 | 仅 30 秒 smoke |
| archive | 合并领域 spec 基线 | 只更新 META.md | 更新 META.md + 归档 snippets |
| 适用场景 | 核心模块、高风险、长期维护 | 原型、低风险小改动 | 临时脚本、验证想法、内部工具 |

### 成本对比表（估算）

| 成本项 | 思考模式 | 省 token 模式 | 性价比模式 |
|---|---|---|---|
| 文档页数 | 3-6 页 | 1-2 页 | 0-1 页 |
| 对话轮数 | 多 | 中 | 少 |
| 产物文件数 | 5-10 个 | 3-5 个 | 2-4 个 |
| 审核节点 | 1-2 个 | 0-1 个 | 0 个 |
| 扫描命令数 | 3-6 个 | 2 个 | 1 个 smoke |
| 规范沉淀 | 完整 | 可选 | snippets |

---

## 阶段一：需求澄清 — `/opsx:explore`

当需求模糊、边界不清或缺少验收标准时执行；需求已明确则跳过。

1. 调用 Superpowers brainstorm 能力（以 `/opsx:explore` 形式执行）。
2. 主动澄清不清晰点，输出结构化 BrainstormDraft。
3. 草稿仅保存在当前对话上下文/内存变量中，**不写任何本地文件**。
4. 草稿至少包含：业务目标、用户场景、2 个以上候选方案、推荐方案及理由、风险与依赖、待确认问题。

**性价比模式额外产物目录**：

```text
.cost-upgrader/
├── changes/
│   └── {YYYYMMDD-<feature>}/
│       ├── META.md          # change 元数据（mode=practical）
│       ├── plan.md          # 一页方案，≤ 30 行
│       ├── TASKS.md         # 任务列表，≤ 10 条
│       └── smoke-report.md  # smoke 结果 + 成本账
└── snippets/
    └── <feature>-<n>.md     # 可复用片段：问题 → 方案 → 代码 → 成本
```

---

## 阶段二：生成规范 — `/opsx:propose`

### 2.1 change 命名

1. 自动按 `YYYYMMDD-<short-kebab-feature>` 生成 change_name，例如 `20260623-order-list-status-filter`。
2. 若用户已指定名称，直接使用；若名称冲突，提示用户调整。
3. 创建目录：
   - 思考模式 / 省 token 模式：`openspec/changes/{change_name}/`
   - 性价比模式：`.cost-upgrader/changes/{change_name}/`

### 2.2 风险分级

生成规范的同时，根据以下维度自动判定风险等级，并询问用户确认：

| 等级 | 判定条件 | 人工门禁策略 | 智能校验门禁策略 |
|------|----------|--------------|------------------|
| low | 纯新增功能、不涉及敏感数据/权限/公共 API/性能瓶颈 | 跳过关卡①；redline 走轻量扫描 | ①-A 智能校验通过 → 直接进 apply；产物附 `awaiting human opt-in` 标记 |
| medium | 普通业务功能，涉及用户数据或内部 API | 默认流程：关卡① + 标准 redline | ①-A 智能校验 + 风险点摘要；高置信度通过则进 apply（产物附 `awaiting human opt-in`），存疑或 `block` 升级为 ①-B 人工 |
| high | 涉及权限/支付/安全/公共 API/数据迁移/跨服务/性能核心路径 | 关卡① + 额外安全复核 + 完整 redline | ①-A 智能校验仅产出**预审报告**，**强制升级**为 ①-B 人工复核 + 安全复核 |

用户可显式覆盖分级，例如“按高风险处理”。门禁形态由上文“智能校验关键词 / 默认行为”决定，写入 `META.md` 的 `gate_mode` 字段。

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
- 性价比模式：只生成 `plan.md`（≤ 30 行） + `TASKS.md`（≤ 10 条）；**不生成** `proposal.md` / `design.md` / `specs/` / `features/`。

### 2.4 META.md 模板

```markdown
# Change: {change_name}

- status: proposed
- created_at: YYYY-MM-DD
- mode: think | fast | practical
- risk_level: low | medium | high
- gate_mode: human | auto-review | skipped
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

### 2.8 Gherkin 可执行规格（推荐生成；性价比模式跳过）

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

### 2.9 性价比模式专属模板

#### plan.md 模板

```markdown
# Plan: <功能>

- 目标：一句话
- 范围：只做 A，不做 B
- 方案：选 X，因为便宜（对比其它方案一句话）
- 依赖：已存在 / 新增 Y（理由）
- 风险：Z（降级：手动兜底）
- 验证：`<smoke 命令>`
- 成本：预计 N 分钟，≤ M 个新依赖
```

#### TASKS.md 模板

```markdown
# Tasks: <功能>

1. [ ] <做什么> → 验证：<怎么看它成了>
2. [ ] ...
```

#### smoke-report.md 模板

```markdown
# Smoke Report

- change: <change_name>
- mode: practical
- total_time: X 分钟
- tasks: N/M
- failed_degraded: ...
- new_deps: ...
- new_files: ...
- reusable_snippet: .cost-upgrader/snippets/<feature>-1.md
- cost_summary: 做了什么 / 花了多少 / 怎么复用
```

### 2.10 审核关卡①（三形态：人工 / 智能校验 / 性价比跳过）

`gate_mode` 决定走哪条分支；流程图与下游 `/opsx:apply` 行为据此切换。

- **思考模式**：默认 `auto-review`；用户可切 `human`。
- **省 token 模式**：默认 `human`（low 风险跳过）；用户可切 `auto-review`。
- **性价比模式**：`gate_mode: skipped`；始终跳过关卡①，把审核成本压到零。

#### 2.9.1 智能校验关卡 ①-A（`gate_mode: auto-review`）

适用于：思考模式默认；省 token 模式用户显式开启。

执行步骤：

1. **工具化扫描**：按 `risk_level` 调用 `openspec/config/redline.yml` 中对应命令（与 `/redline-check` 同一套）。
2. **规范一致性自检**（LLM 短摘要，不读全量代码）：
   - `proposal.md` 验收标准 ↔ `tasks.md` 任务映射是否 1:N 覆盖；
   - `design.md` 接口契约 ↔ `tasks.md` 实现计划是否一致；
   - `features/*.feature` 与 `proposal.md` 验收清单是否一一对应；
   - `META.md` `affected_files` 与 `tasks.md` 涉及文件是否一致。
3. **启发式风险点**（仅在 medium / high 时启用）：越权、注入、N+1、敏感数据落盘、跨服务调用幂等性等模式匹配。
4. **产出结构化预审报告** `openspec/changes/{change_name}/preflight-report.md`：

   ```markdown
   # Pre-flight Report

   - gate_mode: auto-review
   - risk_level: low | medium | high
   - verdict: pass | warn | block
   - confidence: 0.0-1.0
   - tools: <已执行命令与退出码>
   - findings:
     - [severity] 描述 + 证据位置（文件:行号 / 命令输出片段）
   - awaiting_human_opt_in: true | false
   ```

5. **决策矩阵**：

   | 风险等级 | verdict | 行为 |
   |----------|---------|------|
   | low      | pass    | 直接进 apply；`awaiting_human_opt_in: true` 写入报告 |
   | low      | warn / block | 升级为 ①-B 人工 |
   | medium   | pass 且 confidence ≥ 0.8 | 进 apply；`awaiting_human_opt_in: true` |
   | medium   | pass 但 confidence < 0.8 / warn / block | 升级为 ①-B 人工 |
   | high     | 任意 | **强制** 升级为 ①-B 人工 + 安全复核；①-A 仅作预审 |

6. 用户可在 apply 启动前任意时刻回复“暂停 / 我来看一下”接管为 ①-B 人工。

#### 2.9.2 人工复核关卡 ①-B（`gate_mode: human` 或被 ①-A 升级）

- **low 风险**：默认跳过本关卡，直接告诉用户“已按低风险进入 apply，如需审核可回复‘暂停’”。
- **medium / high 风险**：主动停止并请求用户审核。仅当用户明确回复“通过” / “approve” / “ok” / “继续” / “进入 apply” 时，方可继续。
- 若用户提出修改意见，按意见更新 `proposal.md` / `design.md` / `tasks.md` / `specs/` / `features/`，更新后再次请求审核，直至通过。
- high 风险时还需附“额外安全复核”结论（SAST / 敏感操作 / 数据迁移回滚预案），方可放行。

#### 2.9.3 切换规则

- 用户在同一次会话中可说“关闭智能校验 / 走人工”或“开启智能校验”切换 `gate_mode`，需回写 `META.md` 并保留切换时间戳在 `preflight-report.md` 末尾的 `## Gate Switch Log` 段落。
- 切换只允许向前（人工→智能校验或反向），不静默自动切换。

---

## 阶段三：受控实现 — `/opsx:apply`

用户通过关卡①后进入实现阶段。不同模式执行策略不同：

- **思考模式 / 省 token 模式**：以 Superpowers TDD 能力执行。`preflight-report.md` 中的 `findings` 须随每个 task 的完成报告一并回传，便于 apply 阶段重点关照。
- **性价比模式**：不强制 TDD，采用“最小代码 → smoke test → 修到能跑”的短循环。每次只实现一个 task，完成后打一个 `[x]`。

### 3.1 前置读取

1. 读取规范文档：
   - 思考模式 / 省 token 模式：`openspec/changes/{change_name}/` 下全部文档；
   - 性价比模式：`.cost-upgrader/changes/{change_name}/plan.md` + `TASKS.md`。
2. 在内存中按依赖顺序建立任务队列。
3. 思考模式读取 `features/*.feature` 作为验收测试输入；性价比模式跳过。

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
- 性价比模式：每个 task 完成后报告“做了什么、 smoke 是否通过、花了多少 token/时间、新增多少文件/依赖”。

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

practical:
  - name: smoke
    cmd: <项目自定义 smoke 命令，例如 npm run smoke 或 python smoke.py>
    block_on_failure: false
    timeout_seconds: 30
```

### 4.2 执行规则

1. 按风险等级/模式选择对应命令列表：
   - 思考模式：按 `risk_level` 执行完整列表；
   - 省 token 模式：只执行 `low` 级别命令；
   - 性价比模式：只执行一次 ≤ 30 秒的 smoke test。
2. 顺序执行每条命令；失败时立即停止，报告命令输出、失败文件、修复建议。
3. 所有命令通过后：
   - 思考模式：再用 LLM 做补充上下文审计（如权限边界、业务逻辑漏洞）。
   - 省 token 模式：跳过 LLM 审计，或仅对失败命令输出做快速摘要。
   - 性价比模式：不做 LLM 审计，只记录 smoke 结果。
4. 发现阻断项：修复后重新 `/redline-check`。
5. 仅存在建议项：可继续，但在总结中列出。

**省 token 模式额外简化**：

- 只执行 `low` 级别的命令（lint + 单元测试），不执行 secret-scan / SAST / 依赖审计。

**性价比模式额外简化**：

- 不读取 `redline.yml`，只运行一个用户可感知的 smoke 命令（例如 `python script.py`、`curl localhost:3000`）。
- smoke 失败时最多修 3 轮；仍失败则标记为“手动步骤”，不阻塞后续 task。

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

## 阶段五：功能验收关卡④（三形态：人工 / 智能校验 / 性价比跳过）

红线通过后请求验收。`gate_mode` 与 `mode` 共同决定走哪条分支。

### 5.1 人工验收（`gate_mode: human`）

- 思考模式：用户对照 `proposal.md` 和 `features/*.feature` 的验收标准逐项验证。仅当用户明确回复“通过” / “approve” / “ok” / “归档” 时，方可执行 `/opsx:archive`。
- 省 token 模式：只问一句“功能是否符合需求？”；用户确认“是/通过/ok”即可归档。
- 性价比模式：只问一句“功能是否符合需求？”；用户说“不用验收”可直接归档。
- 验收不通过时，回到 `/opsx:apply` 或 `/redline-check` 循环修复，直到通过。

### 5.2 智能校验验收（`gate_mode: auto-review`）

- 仅在思考模式（或省 token 模式用户显式开启）下生效。
- 执行步骤：
  1. 调起 `redline.yml` 中与 `risk_level` 对应的命令复跑一次（保险）。
  2. LLM 逐项对照 `proposal.md` 验收清单与 `features/*.feature` 场景，给出 ✅/❌ 与证据（任务 ID、测试结果、相关文件:行号）。
  3. 追加写入 `preflight-report.md` 的 `## Acceptance Check` 段落，字段：

     ```markdown
     ## Acceptance Check
     - verdict: pass | warn | block
     - confidence: 0.0-1.0
     - ac_results:
       - AC-1: pass | fail (evidence: ...)
       - AC-2: ...
     - awaiting_human_opt_in: true | false
     ```

  4. **决策矩阵**：

     | 风险等级 | verdict | 行为 |
     |----------|---------|------|
     | low      | pass    | 直接进 archive；`awaiting_human_opt_in: true` |
     | low      | warn / block | 升级为人工验收 |
     | medium   | pass 且 confidence ≥ 0.8 | 进 archive；`awaiting_human_opt_in: true` |
     | medium   | 其它 | 升级为人工验收 |
     | high     | 任意 | **强制** 升级为人工验收 |

- 用户可在归档前任意时刻回复“暂停 / 我来看一下”接管为人工验收。
- 验收不通过时，回到 `/opsx:apply` 或 `/redline-check` 循环修复，并重跑本关卡。

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

### 性价比模式

1. 更新 `.cost-upgrader/changes/{change_name}/META.md` 的 `status` 为 `archived`，补充 `archived_at` 和 `affected_files`。
2. **不合并** `openspec/specs/` 基线；把本次可复用片段归档到 `.cost-upgrader/snippets/<feature>-<n>.md`，格式：
   ```markdown
   # <问题>

   ## 方案
   <一句话>

   ## 代码
   ```<lang>
   <代码>
   ```

   ## 成本
   - 依赖：...
   - 时间：...
   - 限制：...
   ```
3. 输出三行总结：
   - 做了什么；
   - 花了多少（token 估算 + 时间 + 新增文件/依赖）；
   - 怎么复用（指向 snippets 路径）。

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

### 思考模式 / 省 token 模式

- [ ] `META.md`、`proposal.md`、`design.md`、`tasks.md`、`specs/`、`features/` 在编码阶段未被修改。
- [ ] 所有 tasks 都有对应测试，且测试全部通过。
- [ ] `/redline-check` 无阻断项。
- [ ] 用户通过关卡④验收。
- [ ] `/opsx:archive` 已执行，`META.md` 已标记 `status: archived` 和 `affected_files`。

### 性价比模式

- [ ] `plan.md`、`TASKS.md` 在编码阶段未被修改。
- [ ] 每个 task 至少通过一次 smoke test，失败项已降级为“手动步骤”。
- [ ] `smoke-report.md` 已生成，含成本账。
- [ ] `/opsx:archive` 已执行，`META.md` 已标记 `status: archived` 和 `affected_files`。
- [ ] 可复用片段已归档到 `.cost-upgrader/snippets/`。

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
| 性价比模式下仍生成 proposal/design/features/specs | 只生成 plan.md + TASKS.md |
| 性价比模式写多个测试文件才跑 smoke | 先跑 smoke，用户明确要测试再补 |
| 性价比模式引入超过 1 个新依赖 | 必须说明理由或换方案 |
| 性价比模式把简单脚本做成通用框架 | 保持脚本级，不抽象 |

---

## 一键口令示例

### 省 token 模式（显式选择）

> “快速模式：帮我用 Superpowers + OpenSpec 跑一遍订单列表状态筛选。”

明确出现“快速模式”关键词后，走轻量流程：

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

### 思考模式（完整门禁）

> “思考模式：帮我用 Superpowers + OpenSpec 完整实现订单列表状态筛选，要认真设计并沉淀规范。”

明确出现“思考模式”关键词后，走完整约束流程：

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

### 性价比模式（显式选择）

> “省钱做：帮我用 Superpowers + OpenSpec 写一个能把 CSV 转成 JSON 的脚本，简单能跑就行。”

明确出现“省钱做 / 简单能跑就行”关键词后，走最低成本流程：

```text
跳过 /opsx:explore
    ↓
/opsx:propose → 只生成 .cost-upgrader/changes/{change_name}/plan.md + TASKS.md
    ↓
跳过关卡①
    ↓
/opsx:apply（先写最小代码 → smoke test → 修到能跑）
    ↓
编译/测试门禁②（简化为一次 smoke）
    ↓
/redline-check（仅 smoke，失败 3 轮降级手动）
    ↓
关卡④（一问确认，或用户说“不用验收”则跳过）
    ↓
/opsx:archive → 更新 META.md，归档 snippets 到 .cost-upgrader/snippets/
    ↓
输出三行总结（做了什么 / 花了多少 / 怎么复用）
```

### 未选择模式（Skill 必须询问）

> “帮我用 Superpowers + OpenSpec 实现订单列表状态筛选。”

用户只激活了 Skill，但没选模式。Skill 必须停止并回复：

```text
请选择运行模式：
1. 思考模式：完整需求/设计/验收标准 + 完整门禁（适合重要功能）
2. 省 token 模式：最简任务列表 + 最轻门禁（适合原型/小改动）
3. 性价比模式：最低成本跑起来 + 极简产物（适合临时脚本/验证想法）

请回复“思考模式”、“快速模式”或“省钱做”。
```

---

## 版本变更日志（CHANGELOG）

### v3.4.0

- 新增「性价比模式（practical mode）」：最低成本交付，产物收敛到 `.cost-upgrader/`。
- 模式选择从二选一升为三选一；新增模式速查表与成本对比表。
- 门禁形态从"人工/智能校验"升级为"自适应门禁"：思考模式默认智能校验、省 token 模式默认人工、性价比模式跳过。
- 新增 `gate_mode: skipped`；新增 mode × gate_mode 默认矩阵。
- 新增性价比模式专属模板：`plan.md`、`TASKS.md`、`smoke-report.md`。
- `redline.yml` 配置示例新增 `practical` 级别。
- 完成定义拆分为"思考/省 token"与"性价比"两套。
- 反模式表新增 4 条性价比红线。
- 一键口令示例新增性价比模式完整流程。
