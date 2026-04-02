# Skills 索引文件 - AI 工具快速查找指南

## 快速索引

当需要使用 Skills 时，可以通过以下方式快速定位：

### JSON 索引（推荐）

读取根目录的 `skills-index.json` 获取完整的 Skills 列表：

```json
{
  "version": "1.0",
  "total_count": 89,
  "by_category": {
    "product": { "name": "Product Manager", "skills": [...] },
    "agile": { "name": "Agile Delivery", "skills": [...] },
    ...
  }
}
```

### Markdown 目录

读取 `skills-catalog.md` 获取人类可读的 Skills 目录。

### 按需加载

每个 Skill 都是独立的 `SKILL.md` 文件，位于对应的分类目录下。

## 分类结构

```
skills/
├── product/           # 产品经理技能 (47+)
│   ├── user-story/
│   ├── backlog-groomer/
│   └── ...
│
├── agile/             # 敏捷交付 (11)
│   ├── sprint-goal-writer/
│   ├── backlog-groomer/
│   └── ...
│
├── scrum/             # Scrum团队 (14)
│   ├── sprint-planning/
│   ├── retrospective/
│   └── ...
│
├── ddd/               # DDD架构 (1)
│   └── SKILL.md
│
├── dev-quality/       # 开发质量 (4)
│   ├── clean-code/
│   ├── debugger/
│   └── ...
│
├── qa-testing/        # QA测试 (10)
│   ├── test-strategy/
│   ├── playwright-automation/
│   └── ...
│
├── api-design/        # API设计 (1)
│   └── api-generator/
│
└── ai-product/        # AI产品 (1)
    └── ai-product/
```

## 使用示例

### 在 Claude Code 中使用

```
@skills/product/backlog-groomer
帮我梳理这个Sprint的Backlog
```

### 在 Cursor 中使用

```
/skill product/backlog-groomer
帮我梳理这个Sprint的Backlog
```

### 直接读取 Skill 内容

```
读取 skills/agile/backlog-groomer/SKILL.md
```

## Skill 格式

每个 Skill 遵循统一格式：

```markdown
---
name: "skill-name"
category: "product|agile|scrum|..."
description: "简短描述"
---

# Skill Name

## Purpose
做什么，何时使用

## Key Concepts
核心概念

## Application
使用步骤

## Examples
示例

## Common Pitfalls
常见错误
```
