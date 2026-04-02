# Learning Open Source - Skills Repository

这是一个软件产品研发流程 Skills 的集合仓库，包含来自多个优秀开源项目的 Skills。

## 项目结构

```
learning-open-source/
├── skills/              # 产品经理技能 (47+)
├── agile-skills/        # 敏捷交付技能 (11)
├── scrum-skills/       # Scrum团队技能 (14)
├── ddd-skills/         # DDD架构技能 (1)
├── dev-quality-skills/ # 开发质量技能 (4)
├── qa-testing-skills/  # QA测试技能 (10)
├── api-design-skills/   # API设计技能 (1)
├── ai-product-skills/   # AI产品技能 (1)
├── skills-index.json    # Skills索引 (JSON)
├── skills-catalog.md    # Skills目录 (Markdown)
├── scripts/            # 工具脚本
│   ├── build_skills_index.py    # 构建索引
│   └── scan_github_skills.py    # 扫描GitHub
└── SKILLS_INDEX.md    # AI工具使用指南
```

## 快速索引

### 读取索引

用户请求时，首先读取 `skills-index.json` 了解可用的 Skills：

```bash
cat skills-index.json
```

或读取 `skills-catalog.md` 获取人类可读的目录。

### 按分类查找 Skills

| 需求 | 目录 | 示例 |
|------|------|------|
| 需求分析、PRD | `skills/` | backlog-groomer, user-story |
| Sprint规划 | `agile-skills/` | sprint-goal-writer, story-splitting |
| Scrum仪式 | `scrum-skills/` | sprint-planning, retrospective |
| 架构设计 | `ddd-skills/` | DDD六边形架构 |
| 代码质量 | `dev-quality-skills/` | clean-code, debugger |
| 测试 | `qa-testing-skills/` | test-strategy, playwright |
| API设计 | `api-design-skills/` | api-generator |
| AI产品 | `ai-product-skills/` | ai-product |

### 使用 Skill

找到需要的 Skill 后，读取其 SKILL.md 文件：

```
skills/agile/backlog-groomer/SKILL.md
```

## Skill 格式

```markdown
---
name: "backlog-groomer"
description: "待办列表梳理"
---

# Backlog Groomer

## Purpose
...
```

## 来源

- **Product Manager Skills**: deanpeters/Product-Manager-Skills
- **Agile Delivery Skills**: 45ck/agile-delivery-skills
- **Scrum Team Skills**: sohei56/claude-scrum-team
- **DDD Skills**: fuzhengwei/xfg-ddd-skills
- **QA Skills**: petrkindlmann/qa-skills
- **Testing Toolkit**: magallon/testing-toolkit
- **API Generator**: smouj/api-generator-skill
- **Awesome Skills**: sickn33/antigravity-awesome-skills

## 工具脚本

### 构建索引

```bash
python scripts/build_skills_index.py
```

### 扫描 GitHub 新 Skills

```bash
python scripts/scan_github_skills.py
```
