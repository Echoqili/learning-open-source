# Skills Repository Structure

## 目录结构

```
learning-open-source/
├── all-skills/          # 主技能文件夹 (所有技能的统一入口，共 149 个)
│   ├── agile-skills/    # 敏捷开发技能 (11)
│   ├── ai-product-skills/  # AI产品技能 (1)
│   ├── ai-safety-skills/   # AI安全技能 (4)
│   ├── api-design-skills/  # API设计技能 (1)
│   ├── ddd-skills/         # DDD领域驱动设计 (1)
│   ├── design-skills/       # 设计技能 (2)
│   ├── dev-quality-skills/  # 开发质量技能 (4)
│   ├── dev-workflow-skills/ # 开发工作流技能 (6)
│   ├── indie-hacker-skills/ # 独立开发者技能 (10)
│   ├── qa-testing-skills/  # QA测试技能 (10)
│   ├── scrum-skills/        # Scrum敏捷技能 (14)
│   ├── skill-creation/      # 技能创建 (1)
│   ├── superpowers-skills/  # 超级能力技能 (6)
│   ├── skills/              # 产品管理 + 工具类技能 (78)
│   │   ├── [47 个产品经理技能]
│   │   ├── tavily-search/        # 搜索 & 研究 (5)
│   │   ├── web-search-pro/
│   │   ├── deep-research/
│   │   ├── baidu-search/
│   │   ├── apify-scraper/
│   │   ├── github-api/           # 开发工具 (8)
│   │   ├── git-commit-automation/
│   │   ├── copilot-cli/
│   │   ├── security-audit-toolkit/
│   │   ├── web-deploy-github/
│   │   ├── n8n-workflow/
│   │   ├── sqlite-agent/
│   │   ├── jira-skill/
│   │   ├── prompt-optimizer/     # AI 工具 (3)
│   │   ├── rag-search/
│   │   ├── ai-code-review/
│   │   ├── excel-analyzer/       # 数据 & 分析 (5)
│   │   ├── google-search-console/
│   │   ├── ga4-analytics/
│   │   ├── stock-analysis/
│   │   ├── bilibili-analytics/
│   │   ├── notion-api/           # 生产力 (10)
│   │   ├── slack-api/
│   │   ├── todoist-api/
│   │   ├── imap-email/
│   │   ├── youtube-analytics/
│   │   ├── wechat-publisher/
│   │   ├── feishu-bitable-api/
│   │   ├── linkedin-lead-gen/
│   │   ├── changelog-generator/
│   │   └── pentest-skill/
│   └── README.md
├── scripts/              # 辅助脚本
│   ├── skill_finder.py           # 技能查找器
│   ├── build_skills_index.py      # 构建索引
│   ├── scan_github_skills.py      # 扫描GitHub
│   ├── skills_index_manager.py    # 索引管理
│   └── skills_security_scanner.py # 安全扫描
└── AI-AGENT-SKILLS.md    # 技能汇总文档
```

## 技能分类

### 1. agile-skills (11 files)
- 敏捷开发相关技能

### 2. ai-product-skills (1 file)
- AI产品管理

### 3. ai-safety-skills (4 files)
- AI安全相关

### 4. api-design-skills (1 file)
- API设计

### 5. ddd-skills (3 files)
- 领域驱动设计

### 6. design-skills (29 files)
- UI/UX设计

### 7. dev-quality-skills (5 files)
- 代码质量

### 8. dev-workflow-skills (8 files)
- 开发工作流

### 9. indie-hacker-skills (10 files)
- 独立开发者技能

### 10. qa-testing-skills (26 files)
- QA与测试

### 11. scrum-skills (14 files)
- Scrum团队技能

### 12. skill-creation (18 files)
- 如何创建技能

### 13. skills (46 skills, 113 files)
- 产品管理技能
- 包含: 用户故事、产品策略、优先级管理等

### 14. superpowers-skills (26 files)
- 超级能力技能
- 包含: 头脑风暴、代码审查、TDD、Git工作流

## 使用方式

### 方式1: 使用 skill_finder.py 查找技能

```bash
python scripts/skill_finder.py --package-scenario tdd
```

### 方式2: 直接浏览 all-skills 文件夹

```bash
# 查看所有技能包
ls all-skills/

# 查看特定技能包内容
ls all-skills/scrum-skills/
```

### 方式3: 安装到 Claude Code

```bash
# 克隆到 Claude Code 技能目录
git clone https://github.com/Echoqili/learning-open-source.git ~/.claude/skills
```
