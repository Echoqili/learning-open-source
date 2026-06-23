---
name: "superpowers-openspec-pipeline"
description: "当用户想要用 Superpowers + OpenSpec(speckit) 跑完整 change 流水线时调用：explore 脑暴 → propose 生成规范（人工审核） → apply TDD 编码 → redline-check 红线校验 → 人工验收 → archive 归档。全程靠门禁卡点防止 AI 漂移。"
license: MIT
compatibility: "纯 Prompt 驱动，需配合 OpenSpec change 工作流使用；所有产物收敛到 openspec/changes/{change_name}/。"
metadata:
  version: "2.0.0"
  author: "自定义总控串联 Skill"
---

# Superpowers + OpenSpec(speckit) 总控串联 Skill

## 触发条件

当用户表达以下任一意图时激活本 Skill：

- “用 Superpowers + OpenSpec 跑一遍”
- “启动总控 Skill / 启动 change 流水线”
- “帮我走 /opsx:explore → /opsx:propose → /opsx:apply → archive”
- 输入原始业务需求并准备进入完整开发流水线

## 核心原则

1. **目录收敛**：所有 change 产物统一存放在 `openspec/changes/{change_name}/`，archive 后合并到全局 spec 基线。
2. **门禁隔离**：
   - `/opsx:explore` 只产内存草稿，**不写任何本地文件**。
   - `/opsx:propose` 只写规范文档，**不写代码**；写完后必须等待**人工审核关卡①**通过。
   - `/opsx:apply` 只新增代码/测试，**禁止修改 changes 目录下的 proposal/design/tasks/specs**；自动通过**编译门禁关卡②**。
   - `/redline-check` 执行红线扫描，存在阻断项则**终止流程**（关卡③）。
   - 人工功能验收关卡④通过后，才能执行 `/opsx:archive`。
3. **测试先行**：每个 task 必须先写测试（Red），再写实现（Green），测试失败时只改代码不改规范。
4. **归档闭环**：验收通过的 change 必须 archive，把本次 spec 增量合并进全局 spec 基线，长期抑制 AI 漂移。

## 执行总序

```text
原始需求输入
    │
    ├─ 需求模糊？ ──是──> /opsx:explore（Superpowers 脑暴，无文件落地）
    │                       │
    │                       否 或 脑暴完成且需求已清晰
    │                       ▼
    │            /opsx:propose（生成 change 规范文档）
    │                       │
    │            人工审核关卡①（必须显式 approve 才能继续）
    │                       ▼
    │            /opsx:apply（强制 TDD 模式执行 tasks）
    │                       │
    │            编译门禁关卡②（自动运行测试/编译，失败即拦截）
    │                       ▼
    │            /redline-check（红线自检关卡③）
    │                       │
    │            存在阻断项？ ──是──> 修复后重新 redline-check
    │                       否
    │                       ▼
    │            人工功能验收关卡④（必须显式 approve 才能归档）
    │                       ▼
    │            /opsx:archive（归档，合并全局 spec 基线）
    │                       ▼
    │            输出总结报告
```

---

## 阶段一：需求澄清 — `/opsx:explore`

当需求模糊、边界不清或缺少验收标准时执行；若需求已明确，可跳过本阶段。

1. 调用 Superpowers brainstorm 能力（以 `/opsx:explore` 形式执行）。
2. 接收用户原始需求，主动澄清不清晰点。
3. 输出 **结构化 BrainstormDraft**，仅保存在当前对话上下文/内存变量中，**严禁写入本地任何文件**。
4. 草稿内容应包含：
   - 业务目标与成功标准
   - 用户场景与关键路径
   - 候选方案发散（至少 2 个）
   - 推荐方案及理由
   - 主要风险、依赖、降级方案
   - 待确认问题（如有）

BrainstormDraft 输出格式示例：

```markdown
# BrainstormDraft

## 目标
...
## 用户场景
...
## 候选方案
- 方案 A：...
- 方案 B：...
## 推荐方案
...
## 风险与依赖
...
## 待确认问题
...
```

---

## 阶段二：生成规范 — `/opsx:propose`

以 OpenSpec(speckit) propose 工作流角色执行，输入为 BrainstormDraft（或直接为明确需求）。

### 2.1 change 命名与目录

1. 自动根据功能生成 `change_name`（短横线连接的小写英文，如 `order-list-status-filter`）；若用户已指定则直接使用。
2. 创建目录：
   ```text
   openspec/changes/{change_name}/
   ```
3. 在该目录下生成规范文档：
   - `proposal.md`：需求提案（对应原 `spec.md`，proposal 层）
   - `design.md`：设计方案（对应原 `plan.md`，design 层）
   - `tasks.md`：任务拆分（tasks 层）
   - `specs/`（可选）：对全局 spec 的增量/修改文件；若本次 change 只涉及新需求且无既有 spec 可忽略

### 2.2 proposal.md 模板

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

### 2.3 design.md 模板

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

### 2.4 tasks.md 模板

```markdown
# Tasks: <功能标题>

> 说明：本表由 `/opsx:propose` 生成，编码阶段仅作为执行蓝图，**不得修改本文档内容**。

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

### 2.5 人工审核关卡①

文档生成后必须**主动停止并请求用户审核**。仅当用户明确回复以下任一表述时，方可继续：

- “通过” / “approve” / “ok” / “继续” / “进入 apply”

若用户提出修改意见，则按意见更新 `proposal.md` / `design.md` / `tasks.md` / `specs/`，更新后再次请求审核，直至通过。

---

## 阶段三：受控实现 — `/opsx:apply`

用户通过关卡①后，以 Superpowers TDD 能力执行本阶段。

### 3.1 前置读取

1. 读取 `openspec/changes/{change_name}/` 下的全部规范文档。
2. 在内存中建立任务队列，按 `tasks.md` 的依赖顺序排列。

### 3.2 每个任务的 TDD 循环

对每个任务执行：

1. **Red**：先写测试用例，运行并确认失败。
2. **Green**：编写最少量业务代码使测试通过。
3. **Run / 编译门禁关卡②**：运行对应测试/编译命令；若失败，仅修改代码/测试，**不修改 changes 目录下任何规范文档**。
4. **Refactor**：在测试通过前提下重构，保持行为不变。

### 3.3 硬性约束

- **仅新增**：代码文件、测试文件、测试用例、配置文件、依赖声明。
- **禁止修改**：`openspec/changes/{change_name}/` 下的 `proposal.md`、`design.md`、`tasks.md` 以及 `specs/` 中的任何已有内容。
- **禁止新增需求**：不得实现未在 `proposal.md` 验收标准中列出的功能。
- **禁止改方案**：技术选型、模块划分、接口契约必须遵循 `design.md`。
- **禁止跳测**：每个 task 至少对应一个可运行的测试用例。
- **测试框架/语言**：严格遵循 `design.md` 中的选型。

### 3.4 完成报告

每完成一个任务，在对话中简要报告：

- 任务 ID 与描述
- 新增/修改的代码与测试文件
- 测试结果摘要（通过/失败数）

---

## 阶段四：红线自检 — `/redline-check`

全部 tasks 完成后，自动执行 `/redline-check`。

### 4.1 扫描范围（示例，可随项目扩展）

| 红线项 | 检查内容 |
|--------|----------|
| 多租户隔离 | 查询是否带 tenant 过滤，跨租户数据访问是否被拦截 |
| 入参 DTO | 是否使用强类型 DTO/Request 对象，是否校验必填/格式/范围 |
| SQL 规范 | 是否存在 SQL 注入风险、N+1 查询、慢查询、缺少索引提示 |
| 权限/auth | 接口是否鉴权，敏感操作是否有权限校验 |
| 敏感信息 | 是否硬编码密钥、token、密码 |
| 异常处理 | 是否捕获并规范化异常，是否泄露内部堆栈 |
| 日志 | 是否记录关键操作，是否避免打印敏感字段 |
| 并发/幂等 | 关键操作是否考虑并发、幂等、分布式锁 |

### 4.2 处理规则

- 发现**阻断项**：立即停止后续流程，向用户报告问题、文件位置、修复建议，等待修复后重新执行 `/redline-check`。
- 仅存在**建议项**：可继续，但需在总结中列出供用户参考。
- 红线全部通过后，方可进入人工功能验收。

---

## 阶段五：人工功能验收关卡④

红线通过后，请求用户进行功能验收：

- 用户对照 `proposal.md` 的验收标准逐项验证。
- 仅当用户明确回复“通过” / “approve” / “ok” / “归档” 时，方可执行 `/opsx:archive`。
- 若验收不通过，回到 `/opsx:apply` 或 `/redline-check` 循环修复，直到通过。

---

## 阶段六：归档闭环 — `/opsx:archive`

验收通过后执行：

1. 将 `openspec/changes/{change_name}/specs/` 中的增量/变更合并进全局 spec 基线（如 `openspec/spec.md` 或 `openspec/specs/`）。
2. 在 change 目录下生成/更新归档标记（例如 `ARCHIVED.md` 或在 `proposal.md` 顶部标注 `status: archived`）。
3. 可选：将本次 change 的关键设计沉淀到项目 `LESSON.md` / `DEVLOG.md`（如项目使用 devlog skill）。
4. 输出最终总结报告。

---

## 目录与产物规范

```text
openspec/
├── spec.md                          # 全局规范基线（archive 后更新）
├── specs/                           # 全局 spec 模块基线（可选）
│   └── ...
└── changes/
    └── {change_name}/
        ├── proposal.md              # 需求提案（对应原 spec.md）
        ├── design.md                # 设计方案（对应原 plan.md）
        ├── tasks.md                 # 任务拆分
        └── specs/                   # 对全局 spec 的增量/修改（可选）
            └── xxx.md
```

---

## 门禁卡点清单

| 关卡 | 类型 | 命令/动作 | 通过条件 | 失败处理 |
|------|------|-----------|----------|----------|
| ① 方案审核 | 人工 | `/opsx:propose` 后等待用户 | 用户显式 approve | 按意见修改规范后重新审核 |
| ② 编译/测试 | 机器 | `/opsx:apply` 中自动运行 | 测试/编译全部通过 | 仅修改代码/测试，不得改规范 |
| ③ 红线自检 | 机器 | `/redline-check` | 无阻断项 | 修复阻断项后重新 redline-check |
| ④ 功能验收 | 人工 | redline 通过后等待用户 | 用户显式 approve | 回到 apply/redline 修复 |

---

## 反模式（必须避免）

| 反模式 | 正确做法 |
|--------|----------|
| `/opsx:explore` 阶段写出临时方案文档 | 仅保留在内存中 |
| `/opsx:propose` 阶段顺手写代码或测试 | 只写规范文档 |
| 用户未审核就自动进入 `/opsx:apply` | 必须等待关卡①显式通过 |
| `/opsx:apply` 阶段修改 `proposal.md`/`design.md`/`tasks.md` | 禁止修改 changes 目录下任何规范文档 |
| 红线存在阻断项仍进入人工验收 | 必须修复并重新 `/redline-check` |
| 验收未通过就执行 `/opsx:archive` | 必须等待关卡④显式通过 |
| 功能交付后不归档、不更新全局 spec | 必须执行 `/opsx:archive` 合并基线 |
| 实现中临时加入未在 proposal 中的功能 | 超出范围，必须剔除或重新走 propose 流程 |

---

## 一键日常口令示例

用户可以说：

> “帮我用 Superpowers + OpenSpec 流水线实现：用户登录后能看到自己的订单列表，支持按状态筛选。”

本 Skill 自动按以下顺序执行：

```text
/opsx:explore（如需求模糊）
    ↓
/opsx:propose → 等待人工审核①
    ↓
/opsx:apply（TDD） → 编译门禁②
    ↓
/redline-check → 红线门禁③
    ↓
人工功能验收④
    ↓
/opsx:archive → 输出总结
```
