# Learning Open Source

这是一个用于学习开源项目的仓库，同时托管自定义 Trae Skill，帮助在 IDE 内以结构化、低成本的方式完成代码变更。

*学习开源项目，记录成长轨迹。*

---

## 仓库结构

```text
learning-open-source/
├── .trae/skills/                    # Trae Skill 定义
│   └── superpowers-openspec-pipeline/   # 总控串联 Skill
│       └── SKILL.md
├── superpowers-openspec-manual/     # 可视化手册（HTML + 字体）
│   ├── _shared/fonts/
│   └── superpowers-openspec-manual.html
└── README.md                        # 本文件
```

---

## 可用 Skill

### superpowers-openspec-pipeline

把 Superpowers 的脑暴/TDD 能力与 OpenSpec 的 change 工作流串成一条自动化流水线：

```text
explore → propose → apply → redline-check → 验收 → archive
```

#### 触发方式

在 Trae 对话中说出以下任一关键词：

- “用 Superpowers + OpenSpec”
- “启动 change 流水线”
- “帮我走 /opsx:explore → /opsx:propose → /opsx:apply → archive”
- 提到任一 `/opsx:` 命令

#### 三种运行模式

| 模式 | 关键词 | 产物 | 适用场景 |
|---|---|---|---|
| **思考模式** | 思考模式 / 完整流程 / 认真设计 | `proposal.md` + `design.md` + `tasks.md` + `features/` + `specs/` | 核心功能、高风险、需要沉淀规范 |
| **省 token 模式** | 快速模式 / 省 token / 原型 | `proposal.md` + `tasks.md` + 极简 `design.md` | 原型、低风险小改动、快速验证 |
| **性价比模式** | 省钱做 / 性价比 / 最小可行 | `plan.md` + `TASKS.md` + `smoke-report.md` | 临时脚本、内部工具、验证想法 |

#### 一键口令示例

```text
思考模式：帮我用 Superpowers + OpenSpec 完整实现订单列表状态筛选，要认真设计并沉淀规范。
```

```text
快速模式：帮我用 Superpowers + OpenSpec 跑一遍订单列表状态筛选。
```

```text
省钱做：帮我用 Superpowers + OpenSpec 写一个能把 CSV 转成 JSON 的脚本，简单能跑就行。
```

#### 产物目录

- 思考模式 / 省 token 模式：`openspec/changes/{YYYYMMDD-<feature>}/`
- 性价比模式：`.cost-upgrader/changes/{YYYYMMDD-<feature>}/`

---

## 快速开始

1. 在 Trae 中打开本仓库。
2. 输入任意 Skill 触发词（见上）。
3. 按提示选择模式并跟随流水线执行。
4. 完成后查看对应产物目录与总结报告。

---

## 可视化手册

打开 [superpowers-openspec-manual/superpowers-openspec-manual.html](superpowers-openspec-manual/superpowers-openspec-manual.html) 可查看流程图与使用说明的离线版本。

---

## 许可证

MIT
