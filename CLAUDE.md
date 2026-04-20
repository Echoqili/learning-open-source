# Learning Open Source - Development Guidelines

## 项目概述

这是一个软件产品研发流程 Skills 的集合仓库，收集了来自多个优秀开源项目的 Skills，支持 AI 工具快速访问和使用。

## 项目结构

```
learning-open-source/
├── all-skills/                # 整合后的 Skills 目录 (149个)
│   ├── skills/               # 产品经理技能 (47) + 工具类技能 (31)
│   │   ├── tavily-search/    # 搜索 & 研究 (5)
│   │   ├── deep-research/
│   │   ├── baidu-search/
│   │   ├── web-search-pro/
│   │   ├── apify-scraper/
│   │   ├── github-api/       # 开发工具 (8)
│   │   ├── git-commit-automation/
│   │   ├── copilot-cli/
│   │   ├── security-audit-toolkit/
│   │   ├── web-deploy-github/
│   │   ├── n8n-workflow/
│   │   ├── sqlite-agent/
│   │   ├── jira-skill/
│   │   ├── prompt-optimizer/ # AI 工具 (3)
│   │   ├── rag-search/
│   │   ├── ai-code-review/
│   │   ├── excel-analyzer/   # 数据 & 分析 (5)
│   │   ├── google-search-console/
│   │   ├── ga4-analytics/
│   │   ├── stock-analysis/
│   │   ├── bilibili-analytics/
│   │   ├── notion-api/       # 生产力 (10)
│   │   ├── slack-api/
│   │   ├── todoist-api/
│   │   ├── imap-email/
│   │   ├── youtube-analytics/
│   │   ├── wechat-publisher/
│   │   ├── feishu-bitable-api/
│   │   ├── linkedin-lead-gen/
│   │   ├── changelog-generator/
│   │   └── pentest-skill/
│   ├── agile-skills/         # 敏捷交付技能 (11)
│   ├── scrum-skills/         # Scrum团队技能 (14)
│   ├── dev-quality-skills/   # 开发质量技能 (4)
│   ├── qa-testing-skills/    # QA测试技能 (10)
│   ├── indie-hacker-skills/  # 独立开发者技能 (10)
│   ├── ai-safety-skills/     # AI安全技能 (4)
│   └── ...
├── web/                      # Web可视化界面 (Flask)
│   ├── app.py               # Flask应用
│   ├── templates/           # HTML模板
│   └── static/              # CSS/JS静态文件
├── scripts/                 # 工具脚本
│   ├── skill_finder.py      # 智能搜索客户端
│   ├── skill_packager.py    # 打包下载工具
│   ├── build_skills_index.py    # 索引构建
│   ├── scan_github_skills.py    # GitHub扫描
│   └── skills_security_scanner.py # 安全扫描
├── skills-index.json         # Skills索引 (JSON)
├── skills-catalog.md         # Skills目录 (Markdown)
├── pyproject.toml           # 项目配置
└── CLAUDE.md               # 本文件
```

## 技术栈

- **Python**: 3.9+ (Flask Web, 工具脚本)
- **Web**: Flask + HTML/CSS/JavaScript
- **Skills格式**: Markdown + YAML frontmatter
- **CLI**: 交互式TUI客户端

## 命令

```bash
# 启动Web界面
cd web && python app.py
# 访问 http://127.0.0.1:5555

# 启动TUI客户端
python scripts/skill_finder.py

# 构建索引
python scripts/build_skills_index.py

# 安全扫描
python scripts/skills_security_scanner.py

# Lint Python
ruff check scripts/ web/

# 代码格式化
ruff format scripts/ web/
```

## Skills 分类

| 分类 | 数量 | 说明 |
|------|------|------|
| product | 47 | 产品经理技能 |
| scrum | 14 | Scrum仪式 |
| agile | 11 | 敏捷交付 |
| qa-testing | 10 | QA测试 |
| indie-hacker | 10 | 独立开发创业 |
| productivity | 10 | 效率工具集成 (Notion/Slack/飞书等) |
| dev-tools | 8 | 开发工具 (GitHub/Jira/n8n等) |
| dev-workflow | 6 | 开发工作流 |
| superpowers | 6 | Superpowers框架 |
| data-analytics | 5 | 数据分析 (GA4/GSC/Excel等) |
| search-research | 5 | 搜索 & 研究 (Tavily/深度研究等) |
| ai-safety | 4 | AI安全 |
| dev-quality | 4 | 开发质量 |
| ai-tools | 3 | AI工具 (Prompt优化/RAG/代码审查) |
| design | 2 | 设计系统 |
| **总计** | **149** | |

## 代码风格

- **Python**: Ruff格式化, 类型提示, 4空格缩进
- **Markdown**: 2空格缩进YAML, 80字符行宽
- **JSON**: 2空格缩进
- **提交**: 语义化提交格式 (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`)

## Skills 格式

```markdown
---
name: "skill-name"
description: "技能描述"
---
# Skill Name

## Purpose
...
```
