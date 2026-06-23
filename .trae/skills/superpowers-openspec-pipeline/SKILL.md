---
name: "superpowers-openspec-pipeline"
description: "把 Superpowers 的脑暴/TDD 能力与 OpenSpec(speckit) 的 change 工作流串成一条自动化 Skill：explore → propose（人工审核）→ apply（TDD）→ redline-check → 人工验收 → archive。"
license: MIT
compatibility: "纯 Prompt 驱动，需配合 OpenSpec change 工作流使用；产物统一收敛到 openspec/changes/{change_name}/。"
metadata:
  version: "2.1.0"
  author: "自定义总控串联 Skill"
---

# Superpowers + OpenSpec(speckit) 总控串联 Skill

## 触发条件

用户表达以下任一意图时激活：

- “用 Superpowers + OpenSpec 跑一遍”
- “启动 change 流水线”
- “帮我走 /opsx:explore → /opsx:propose → /opsx:apply → archive”
- 输入原始业务需求并准备进入完整开发流水线

## 设计目标

1. 把 AI 的“发散能力”锁死在规范阶段，编码阶段只能按图施工。
2. 用机器门禁（编译、测试、红线扫描）和人工门禁（方案审核、功能验收）替代口头约束。
3. 通过 archive 把每次 change 的约束沉淀为全局 spec 基线，长期抑制 AI 漂移。

## 执行总序

```text
原始需求输入
    │
    ├─ 需求模糊？ ──是──> /opsx:explore（Superpowers 脑暴，不写文件）
    │                       │
    │                       否 或 脑暴完成
    │                       ▼
    │            /opsx:propose（生成 change 规范文档）
    │                       │
    │            人工审核关卡①（用户显式 approve）
    │                       ▼
    │            /opsx:apply（强制 TDD 模式执行 tasks）
    │                       │
    │            编译/测试门禁关卡②（自动运行，失败拦截）
    │                       ▼
    │            /redline-check（红线扫描关卡③）
    │                       │
    │            存在阻断项？ ──是──> 修复后重新 redline-check
    │                       否
    │                       ▼
    │            人工功能验收关卡④（用户显式 approve）
    │                       ▼
    │            /opsx:archive（合并全局 spec 基线）
    │                       ▼
    │            输出总结报告
```

## 产物目录规范

```text
openspec/
├── spec.md                          # 全局规范基线（archive 后更新）
├── specs/                           # 全局 spec 分模块基线（可选）
│   └── ...
└── changes/
    └── {change_name}/
        ├── proposal.md              # 需求提案（对应 spec 层）
        ├── design.md                # 设计方案（对应 design 层）
        ├── tasks.md                 # 任务拆分（对应 tasks 层）
        └── specs/                   # 对全局 spec 的增量/变更（可选）
            └── xxx.md
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

### 2.2 生成文档

在该目录下生成：

- `proposal.md`：需求提案
- `design.md`：设计方案
- `tasks.md`：任务拆分
- `specs/`（可选）：对全局 spec 的增量/修改；若无既有全局 spec，可省略，直接把 proposal.md 作为初始 spec

### 2.3 proposal.md 模板

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

### 2.4 design.md 模板

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

### 2.5 tasks.md 模板

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

### 2.6 人工审核关卡①

文档生成后必须主动停止并请求用户审核。仅当用户明确回复以下表述之一时，方可继续：

- “通过” / “approve” / “ok” / “继续” / “进入 apply”

若用户提出修改意见，按意见更新 `proposal.md` / `design.md` / `tasks.md` / `specs/`，更新后再次请求审核，直至通过。

---

## 阶段三：受控实现 — `/opsx:apply`

用户通过关卡①后，以 Superpowers TDD 能力执行。

### 3.1 前置读取

1. 读取 `openspec/changes/{change_name}/` 下全部规范文档。
2. 在内存中按依赖顺序建立任务队列。

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
- 禁止修改 `openspec/changes/{change_name}/` 下的 `proposal.md`、`design.md`、`tasks.md` 以及 `specs/` 中的已有内容。
- 禁止实现未在 `proposal.md` 验收标准中列出的功能。
- 技术选型、模块划分、接口契约遵循 `design.md`。
- 每个 task 至少对应一个可运行的测试用例。
- 测试框架与语言遵循 `design.md`。

### 3.5 完成报告

每完成一个任务简要报告：任务 ID、新增/修改的代码与测试文件、测试结果摘要。

---

## 阶段四：红线自检 — `/redline-check`

全部 tasks 完成后执行。优先调用项目已配置的真实扫描工具；若项目未配置，再以 LLM 自检兜底。

### 4.1 推荐工具化红线（按项目实际情况启用）

| 红线项 | 推荐工具/手段 |
|--------|--------------|
| 多租户隔离 | 代码审查 + 单元测试断言 |
| 入参 DTO/校验 | 语言级类型检查、schema 校验（如 Zod、Pydantic、Bean Validation） |
| SQL 注入/N+1 | ORM 参数化查询、SQL 静态分析、集成测试 |
| 权限/auth | 框架鉴权中间件、权限单元测试 |
| 敏感信息泄露 | secret scanner（如 gitleaks、GitHub secret scanning） |
| 异常/错误处理 | 静态分析、代码审查 |
| 日志脱敏 | 日志审查规则、lint |
| 并发/幂等 | 代码审查 + 压力/并发测试 |

### 4.2 处理规则

- 发现阻断项：立即停止，报告问题、文件位置、修复建议；修复后重新 `/redline-check`。
- 仅存在建议项：可继续，但需在总结中列出供用户参考。
- 红线全部通过后，方可进入人工功能验收。

---

## 阶段五：人工功能验收关卡④

红线通过后请求用户验收：

- 用户对照 `proposal.md` 的验收标准逐项验证。
- 仅当用户明确回复“通过” / “approve” / “ok” / “归档” 时，方可执行 `/opsx:archive`。
- 验收不通过时，回到 `/opsx:apply` 或 `/redline-check` 循环修复，直到通过。

---

## 阶段六：归档闭环 — `/opsx:archive`

验收通过后执行：

1. 将 `openspec/changes/{change_name}/specs/` 中的增量/变更合并进全局 spec 基线（`openspec/spec.md` 或 `openspec/specs/`）。
2. 在 change 目录下生成 `ARCHIVED.md` 或在 `proposal.md` 顶部标注 `status: archived`。
3. 输出最终总结报告。

---

## 需求中途变更的处理

若在 `/opsx:apply` 或验收阶段发现需求必须调整：

1. 暂停当前阶段，不直接修改 changes 目录下的规范文档。
2. 回到 `/opsx:propose`，按新需求重新生成或更新规范文档。
3. 重新通过人工审核关卡①后，再进入 `/opsx:apply`。

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

- [ ] `proposal.md`、`design.md`、`tasks.md` 在编码阶段未被修改。
- [ ] 所有 tasks 都有对应测试，且测试全部通过。
- [ ] `/redline-check` 无阻断项。
- [ ] 用户通过关卡④验收。
- [ ] `/opsx:archive` 已执行，全局 spec 基线已更新。

---

## 反模式

| 反模式 | 正确做法 |
|--------|----------|
| `/opsx:explore` 写出临时方案文档 | 仅保留在内存中 |
| `/opsx:propose` 顺手写代码或测试 | 只写规范文档 |
| 用户未审核就自动进入 `/opsx:apply` | 必须等待关卡①显式通过 |
| `/opsx:apply` 修改 changes 目录下的规范文档 | 禁止修改，需求变更走重新 propose |
| 红线阻断项仍进入人工验收 | 修复后重新 `/redline-check` |
| 验收未通过就归档 | 必须等待关卡④通过 |
| 不归档、不更新全局 spec | 必须执行 `/opsx:archive` |
| 实现中临时加入未在 proposal 中的功能 | 超出范围，剔除或重新走 propose |

---

## 一键口令示例

> “帮我用 Superpowers + OpenSpec 流水线实现：用户登录后能看到自己的订单列表，支持按状态筛选。”

本 Skill 自动执行：

```text
/opsx:explore（如需求模糊）
    ↓
/opsx:propose → 等待人工审核①
    ↓
/opsx:apply（TDD） → 编译/测试门禁②
    ↓
/redline-check → 红线门禁③
    ↓
人工功能验收④
    ↓
/opsx:archive → 输出总结
```
