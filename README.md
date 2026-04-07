# Learning Open Source

这是一个用于学习开源项目的仓库，收集了软件产品研发流程相关的优秀 Skills。

## 仓库内容

### 1. Product Manager Skills
**来源:** [deanpeters/Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills)

47个经过实战检验的PM技能 + 6个命令工作流，帮助产品经理和AI代理以专业水平执行产品管理工作。

**技能分类：**
- Component Skills (21) - PM工件模板（用户故事、PRD、路线图等）
- Interactive Skills (20) - 自适应引导式发现
- Workflow Skills (6) - 完整端到端PM流程

**框架来源：** Teresa Torres、Jeff Patton、Mike Cohn、Amazon Working Backwards

---

### 2. Agile Delivery Skills
**来源:** [45ck/agile-delivery-skills](https://github.com/45ck/agile-delivery-skills)

敏捷交付技能包，涵盖 Sprint 全生命周期。

**包含技能：**
- `backlog-groomer` - 待办列表梳理
- `sprint-goal-writer` - Sprint 目标编写
- `story-splitting-advisor` - 用户故事拆分指导
- `acceptance-driven-planner` - 验收驱动规划
- `definition-of-done-enforcer` - DoD 执行
- `retrospective-pattern-finder` - 回顾会议模式发现
- `blocker-escalation-advisor` - 障碍升级指导
- `iteration-outcome-reviewer` - 迭代成果审查
- `cross-functional-team-checker` - 跨功能团队检查
- `self-organization-health-check` - 自组织健康检查
- `regression-discipline-checker` - 回归纪律检查

---

### 3. Scrum Team Skills
**来源:** [sohei56/claude-scrum-team](https://github.com/sohei56/claude-scrum-team)

完整的 Scrum 团队 AI 辅助系统，14个仪式技能覆盖 Scrum 全流程。

**包含技能：**
- `requirements-sprint` - 需求整理 Sprint
- `sprint-planning` - Sprint 计划会议
- `backlog-refinement` - 待办列表精化
- `design` - 设计阶段
- `implementation` - 开发实施
- `scaffold-design-spec` - 设计规范脚手架
- `cross-review` - 交叉评审
- `smoke-test` - 冒烟测试
- `sprint-review` - Sprint 评审
- `retrospective` - 回顾会议
- `integration-sprint` - 集成 Sprint
- `change-process` - 变更流程

---

### 4. DDD 六边形架构技能
**来源:** [fuzhengwei/xfg-ddd-skills](https://github.com/fuzhengwei/xfg-ddd-skills)

DDD 六边形架构工程搭建与开发解决方案。

**架构分层：**
```
Trigger → API → Case → Domain ← Infrastructure
```

**核心内容：**
- Domain 纯净性原则
- Entity、Aggregate、VO 设计规范
- Repository/Port-Adapter 模式
- 策略模式、责任链模式落地
- 设计模式适用场景判断

---

### 5. 开发质量技能
**来源:** [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)

软件开发质量相关技能集。

**包含技能：**
- `clean-code` - 整洁代码原则（Bob大叔 Clean Code）
- `debugger` - 调试专家技能
- `database` - 数据库工作流（设计、优化、迁移）
- `github` - GitHub 操作技能

---

### 6. QA 测试技能
**来源:** [petrkindlmann/qa-skills](https://github.com/petrkindlmann/qa-skills)

40个 QA 与测试自动化技能，涵盖测试策略、Playwright、CI/CD 等。

**精选技能：**
- `test-strategy` - 测试策略制定
- `test-planning` - 测试计划制定
- `playwright-automation` - Playwright 端到端测试
- `api-testing` - API 测试
- `unit-testing` - 单元测试
- `security-testing` - 安全测试
- `performance-testing` - 性能测试
- `test-migration` - 测试迁移

---

### 7. 测试策略技能
**来源:** [magallon/testing-toolkit](https://github.com/magallon/testing-toolkit)

与技术栈无关的测试策略和 E2E 测试方法论。

**包含技能：**
- `testing-strategy` - 通用测试策略
- `e2e-testing` - 端到端测试最佳实践

---

### 8. API 设计技能
**来源:** [smouj/api-generator-skill](https://github.com/smouj/api-generator-skill)

从规范生成 REST 和 GraphQL API 的技能。

**包含技能：**
- `api-generator` - 从 OpenAPI 定义生成生产级 API

---

### 9. AI 产品技能
**来源:** [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)

AI 产品开发最佳实践。

**核心内容：**
- 结构化输出与验证
- 流式响应处理
- Prompt 版本控制与测试
- 陷阱防范（幻觉、注入、超量）
- 生产级 AI 特性开发

---

### 10. AI 安全技能
**来源:** 整合自 OWASP、MITRE ATLAS、Basilisk 等权威资源

AI 安全与防护技能集，覆盖 Prompt 注入防御、越狱检测、幻觉检测、AI 红队等。

**包含技能：**
- `prompt-injection-defense` - Prompt 注入攻击检测与防御
- `jailbreak-detection` - 越狱尝试检测与阻断
- `hallucination-detection` - LLM 幻觉检测与缓解
- `ai-red-teaming` - AI 系统红队渗透测试

**核心概念：**
- OWASP LLM Top 10 对齐
- MITRE ATLAS 框架
- 防御纵深架构
- 输入验证与输出过滤
- 不确定性信号

---

### 11. Superpowers 开发框架 ⭐ 136k Stars
**来源:** [obra/superpowers](https://github.com/obra/superpowers)

完整开发工作流框架，TDD 强制执行者。

**精选技能（6个）：**
- `test-driven-development` - 红-绿-重构 TDD 循环
- `systematic-debugging` - 4阶段系统调试法
- `brainstorming` - 苏格拉底式需求探索
- `writing-plans` - 可执行实现计划
- `requesting-code-review` - 提交前审查流程
- `using-git-worktrees` - Git Worktree 隔离开发

---

### 12. Dev Workflow 开发工作流 ⭐ 140k Stars
**来源:** [knibals/everything-claude-code](https://github.com/knibals/everything-claude-code)

Everything Claude Code 核心工作流技能集。

**精选技能（6个）：**
- `tdd-workflow` - 测试驱动开发工作流
- `coding-standards` - 团队编码规范执行
- `git-workflow` - Git 分支策略与协作
- `agentic-engineering` - Agent 工程最佳实践
- `continuous-learning` - 上下文持续学习机制
- `context-budget` - 上下文预算管理

---

### 13. Design System 设计系统 ⭐ 59k Stars
**来源:** [ui-ux-pro-max-skill](https://github.com/ui-ux-pro-max-skill)

专业设计系统生成器，覆盖 161 种行业色板 + 67 种 UI 风格。

**精选技能（2个）：**
- `ui-ux-pro-max` - 全栈设计系统
- `design-system` - 设计系统规范

**特色功能：**
- 161 种行业色板（医疗、金融、电商等）
- 67 种 UI 风格（Material、Flat、Glassmorphism 等）
- 自动输出符合行业规范的设计方案

---

### 14. Skill Authoring 技能开发 ⭐ 官方
**来源:** [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/skill-creator)

Anthropic 官方 Skill 开发工具，含意图捕获→测试→优化全流程。

**核心功能：**
- 意图捕获与需求分析
- Skill 测试与验证
- 可视化效果对比
- subagent 协作模式

---

### 15. Indie Hacker 独立开发者创业 💰
**来源:** 基于 Sahil Lavingia《小而美》提炼

独立开发者/Indie Hacker 创业技能包，覆盖发现→验证→启动→增长全流程。

**包含技能（10个）：**
- `find-community` - 通过社群需求反向推导创业方向
- `validate-idea` - 用预售/众测替代市场调研（48小时验证法）
- `mvp` - 砍掉所有非生存必需功能（Gumroad初期案例）
- `processize` - 先人工模拟流程，手动处理100单后再自动化
- `first-customers` - 逐个攻破前100个用户，拒绝等流量心态
- `pricing` - 定价公式：成本×3 ≤ 定价 ≤ 替代方案价格×0.7
- `marketing-plan` - 每周1篇深度内容+3次互动，极简内容公式
- `grow-sustainably` - 利润增长率≥收入增长率，铁律拒绝烧钱换规模
- `company-values` - 用价值观筛选团队，10x效率招聘过滤器
- `minimalist-review` - 三问过滤器快速决策，极简复盘

**底层逻辑：** 发现社群 → 验证需求 → 手动启动 → 量化增长

---

## 快速导航

| 目录 | 技能数 | 用途 | Stars |
|------|--------|------|-------|
| `skills/` | 47+ | 产品经理技能 | - |
| `agile-skills/` | 11 | 敏捷交付 | - |
| `scrumm-skills/` | 14 | Scrum 团队 | - |
| `ddd-skills/` | 1 | DDD 架构 | - |
| `dev-quality-skills/` | 4 | 开发质量 | - |
| `qa-testing-skills/` | 10 | QA 测试 | - |
| `api-design-skills/` | 1 | API 设计 | - |
| `ai-product-skills/` | 1 | AI 产品 | - |
| `ai-safety-skills/` | 4 | AI 安全 | - |
| `superpowers-skills/` | 6 | TDD/调试/重构 | ⭐ 136k |
| `dev-workflow-skills/` | 6 | 开发工作流 | ⭐ 140k |
| `design-skills/` | 2 | 设计系统 | ⭐ 59k |
| `skill-creation/` | 1 | Skill开发 | 🛠️ 官方 |
| `indie-hacker-skills/` | 10 | 独立开发创业 | 💰 |

---

## 🛡️ 安全扫描与客户端

### 安全扫描引擎

基于 Agent Skills Guard 的安全扫描逻辑，检测 **22 项硬触发规则** 和 **8 大风险类别**：

| 风险类别 | 检测内容 | 硬触发 |
|---------|---------|--------|
| 破坏性操作 | rm -rf /、磁盘擦除 | ✅ |
| 远程代码执行 | curl \| bash、反弹Shell | ✅ |
| 命令注入 | eval()、os.system() | ❌ |
| 网络外传 | 数据外传到远程服务器 | ❌ |
| 权限提升 | sudoers 修改、提权 | ✅ |
| 持久化后门 | crontab、SSH密钥注入 | ✅ |
| 敏感信息泄露 | API Key、Token、密码 | ❌ |
| 敏感文件访问 | ~/.ssh、/etc/shadow | ✅ |

**评分规则：**
- 90-100: ✅ 安全
- 70-89: ⚠️ 低风险
- 50-69: ⚠️ 中等风险
- 30-49: 🔴 高风险
- 0-29: 🚨 严重风险

### 工具脚本

| 脚本 | 功能 |
|------|------|
| `scripts/skill_index_manager.py` | 交互式客户端（浏览/扫描/统计） |
| `scripts/skills_security_scanner.py` | 安全扫描引擎 |
| `scripts/build_skills_index.py` | 索引构建脚本 |
| `scripts/scan_github_skills.py` | GitHub Skills 发现 |

**运行客户端：**
```bash
python scripts/skill_index_manager.py
```

**快速扫描：**
```bash
python scripts/skill_index_manager.py --scan
```

---

*学习开源项目，记录成长轨迹*
