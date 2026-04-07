# Skills Manager 快速启动指南

## 🚀 快速启动

```bash
cd d:\pyworkplace\github\learning-open-source
python scripts/skill_index_manager.py
```

## 📋 功能菜单

| 选项 | 功能 | 说明 |
|------|------|------|
| 1 | 📋 浏览目录 | 按分类查看所有 Skills |
| 2 | 🔨 构建索引 | 重新扫描生成索引 |
| 3 | 🛡️ 安全扫描 | 检测 Skills 安全风险 |
| 4 | 📊 统计信息 | 查看 Skills 数量统计 |
| 5 | ❓ 使用帮助 | 查看帮助文档 |
| 0 | 退出 | 退出程序 |

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
