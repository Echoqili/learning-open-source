# 自动化工作流引擎 (Auto Workflow Engine)

## 创新功能

这是一个超越 superpowers-zh 的创新功能 - 自动工作流引擎，可以根据项目上下文和任务类型自动选择和执行最佳工作流程。

## 核心特性

```
┌─────────────────────────────────────────────────────────────────┐
│                    自动化工作流引擎架构                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📥 输入 ──→ 🎯 意图识别 ──→ 📋 流程规划 ──→ ⚙️ 自动执行        │
│                │                                               │
│                ▼                                               │
│           🔍 上下文感知                                         │
│           • 项目类型                                            │
│           • 技术栈                                             │
│           • 任务类型                                            │
│           • 历史行为                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 工作原理

### 1. 意图识别
```python
# 分析用户输入，识别任务意图
Intent = {
    "type": "feature_request" | "bug_fix" | "refactor" | "code_review",
    "priority": "high" | "medium" | "low",
    "scope": ["前端", "后端", "数据库", "全栈"],
    "complexity": "simple" | "medium" | "complex"
}
```

### 2. 上下文感知
```yaml
context:
  project:
    type: web-app
    framework: react
    language: typescript
    has_tests: true
    has_lint: true

  environment:
    os: windows
    has_docker: true
    has_database: true
```

### 3. 流程匹配
```yaml
workflows:
  feature_request:
    when:
      project.type: web-app
      task.complexity: medium
    steps:
      - skill: requirement-interview
      - skill: writing-plans
      - skill: test-driven-development
      - skill: chinese-code-review

  bug_fix:
    when:
      task.priority: high
    steps:
      - skill: systematic-debugging
      - skill: verification-before-completion
```

## 自动执行示例

### 场景 1: 用户说 "添加用户登录功能"

```
用户: "添加用户登录功能"

🤖 意图识别:
  - 类型: feature_request
  - 范围: 全栈
  - 复杂度: medium

📋 自动选择工作流:
  1. requirement-interview (需求访谈)
  2. writing-plans (编写计划)
  3. code-development (代码开发)
  4. test-driven-development (测试驱动)
  5. chinese-code-review (代码审查)
  6. verification-before-completion (完成验证)

⚙️ 开始执行...
```

### 场景 2: 用户说 "线上出 bug 了"

```
用户: "线上出 bug 了"

🤖 意图识别:
  - 类型: bug_fix
  - 优先级: high
  - 紧急度: urgent

📋 自动选择工作流:
  1. systematic-debugging (系统调试)
  2. verification-before-completion (验证修复)
  3. hotfix-workflow (热修复流程)

⚙️ 开始执行...
```

## 工作流定义

### 标准工作流模板

```yaml
# workflows/feature-development.yaml
name: 功能开发流程
description: 标准的全功能开发工作流

steps:
  - id: 1
    skill: requirement-interview
    auto_params:
      topic: 用户需求
    timeout: 10min

  - id: 2
    skill: writing-plans
    depends_on: [1]
    output: plan.md

  - id: 3
    skill: test-driven-development
    depends_on: [2]
    parallel: true
      - skill: code-development
      - skill: writing-tests

  - id: 4
    skill: verification-before-completion
    depends_on: [3]
```

### 条件分支

```yaml
workflows:
  smart_workflow:
    steps:
      - skill: detect-task-type

      - if: "task.type == 'bug_fix'"
        then:
          - skill: systematic-debugging
          - skill: quick-fix

      - if: "task.type == 'feature'"
        then:
          - skill: requirement-interview
          - skill: writing-plans
          - skill: code-development

      - if: "task.complexity == 'high'"
        then:
          - skill: subagent-driven-development
          - skill: code-review
```

## 智能推荐

### 基于历史的推荐

```python
class WorkflowRecommender:
    def recommend(self, task, context):
        # 分析历史成功案例
        similar_tasks = self.find_similar(task)

        if similar_tasks:
            successful_workflow = similar_tasks[0].workflow
            return f"根据之前类似任务，推荐使用: {successful_workflow}"

        # 基于规则推荐
        return self.rule_based_recommend(task)
```

### 学习优化

```yaml
learning:
  enabled: true
  feedback:
    - after: task_complete
      prompt: "这个工作流执行效果如何？"
     收集: user_rating

  optimization:
    weekly: 分析成功率，调整权重
    monthly: 更新推荐算法
```

## 创新点

### 1. 全自动闭环
- 自动识别意图
- 自动选择工作流
- 自动执行
- 自动验证结果

### 2. 上下文感知
- 理解项目类型
- 理解技术栈
- 理解团队习惯

### 3. 持续学习
- 记录执行结果
- 优化推荐算法
- 适应团队风格

### 4. 人机协作
- 执行过程可视化
- 关键节点确认
- 随时可干预
