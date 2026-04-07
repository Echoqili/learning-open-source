# Skills Manager 快速启动指南

## 🚀 快速启动

### 智能导航（新推荐）
```bash
cd d:\pyworkplace\github\learning-open-source
python scripts/skill_finder.py
```

### 经典菜单客户端
```bash
cd d:\pyworkplace\github\learning-open-source
python scripts/skill_index_manager.py
```

## 🧠 Smart Skills Finder - 智能搜索

根据需求或场景快速找到合适的 Skills：

```bash
# 交互式搜索（推荐）
python scripts/skill_finder.py

# 命令行快速搜索
python scripts/skill_finder.py --search "Sprint规划"
python scripts/skill_finder.py --scenario scrum_team
python scripts/skill_finder.py --category product
```

### 功能说明

| 选项 | 功能 | 说明 |
|------|------|------|
| 1 | 🔍 关键词搜索 | 输入描述快速找到所需 Skills |
| 2 | 🎯 场景化推荐 | 按工作场景获取推荐 Skills |
| 3 | 📂 分类浏览 | 按15个分类查看所有 Skills |
| 4 | 📊 Skills统计 | 查看 Skills 分布情况 |

### 场景化推荐覆盖

| 场景 | 说明 |
|------|------|
| 📋 产品经理基础 | 需求分析、PRD、用户故事 |
| 🎯 高级产品经理 | 战略、指标、商业化 |
| 🔍 客户探索验证 | 访谈准备、发现流程 |
| 🏃 敏捷开发团队 | Sprint规划、回顾 |
| 🎯 Scrum团队 | 14个Scrum仪式 |
| 🧪 QA与测试 | 自动化、E2E、性能 |
| 🏗️ 架构设计 | DDD、API设计 |
| 💎 开发质量 | 整洁代码、调试 |
| ⚡ TDD测试驱动 | 红绿重构、单元测试 |
| 💰 独立开发者 | MVP、获客、增长 |
| 🤖 AI产品开发 | Prompt、安全、幻觉检测 |
| 🎨 设计系统 | UI/UX、组件库 |
| 🛠️ Skill开发 | 官方创建工具 |

## ⚡ 快速命令

### 交互式客户端（带菜单）
```bash
python scripts/skill_index_manager.py
```

### 快速扫描（无菜单）
```bash
python scripts/skill_index_manager.py --scan
```

### 扫描单个 Skill
```bash
python scripts/skills_security_scanner.py skills/user-story
```

### 重新构建索引
```bash
python scripts/build_skills_index.py
```

### 扫描 GitHub 发现新 Skills
```bash
python scripts/scan_github_skills.py
```

## 🛡️ 安全扫描说明

安全扫描检测 **8 大风险类别**：

| 风险等级 | 评分 | 说明 |
|---------|------|------|
| ✅ 安全 | 90-100 | 可放心使用 |
| ⚠️ 低风险 | 70-89 | 轻微风险 |
| ⚠️ 中等风险 | 50-69 | 谨慎使用 |
| 🔴 高风险 | 30-49 | 建议替换 |
| 🚨 严重风险 | 0-29 | 禁止使用 |

**注意**：安全测试类 Skills（如 `security-testing`、`jailbreak-detection`）本身包含攻击代码演示，扫描到风险是正常的。

## 📁 项目结构

```
learning-open-source/
├── skills/                    # 47+ 产品经理技能
├── agile-skills/              # 11 敏捷交付
├── scrum-skills/             # 14 Scrum团队
├── ddd-skills/              # 1 DDD架构
├── dev-quality-skills/      # 4 开发质量
├── qa-testing-skills/       # 10 QA测试
├── api-design-skills/        # 1 API设计
├── ai-product-skills/        # 1 AI产品
├── ai-safety-skills/        # 4 AI安全
├── superpowers-skills/      # 6 Superpowers
├── dev-workflow-skills/     # 6 开发工作流
├── design-skills/           # 2 设计系统
├── skill-creation/          # 1 Skill开发
├── indie-hacker-skills/    # 10 独立开发创业
├── scripts/
│   ├── skill_index_manager.py      # 交互式客户端
│   ├── skills_security_scanner.py  # 安全扫描引擎
│   ├── build_skills_index.py        # 索引构建
│   └── scan_github_skills.py        # GitHub扫描
├── skills-index.json         # Skills索引
├── skills-catalog.md         # Skills目录
└── README.md                 # 项目说明
```

## 🎯 使用场景

| 场景 | 推荐命令 |
|------|---------|
| 日常浏览 Skills | `python scripts/skill_index_manager.py` → 选择 1 |
| 安装前安全检查 | `python scripts/skill_index_manager.py` → 选择 3 |
| 添加新 Skills 后更新索引 | `python scripts/skill_index_manager.py` → 选择 2 |
| 查看统计信息 | `python scripts/skill_index_manager.py` → 选择 4 |
| 发现新 Skills 源 | `python scripts/scan_github_skills.py` |

## 📊 Skills 统计

| 分类 | 数量 | Stars |
|------|------|-------|
| Product Manager | 47+ | - |
| Scrum Team | 14 | - |
| Agile Delivery | 11 | - |
| QA Testing | 10 | - |
| Indie Hacker | 10 | 💰 |
| Superpowers | 6 | ⭐ 136k |
| Dev Workflow | 6 | ⭐ 140k |
| Dev Quality | 4 | - |
| AI Safety | 4 | - |
| Design System | 2 | ⭐ 59k |
| DDD Architecture | 1 | - |
| API Design | 1 | - |
| AI Product | 1 | - |
| Skill Authoring | 1 | 🛠️ 官方 |

**总计：118 个 Skills，覆盖 15 个分类**

---

*学习开源项目，记录成长轨迹*
