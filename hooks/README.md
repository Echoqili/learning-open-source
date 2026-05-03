# Git Hooks 集成

## 概述

Git Hooks 允许在 Git 操作的关键节点自动执行脚本，用于自动化检查、格式化、审查等任务。

## 目录结构

```
.git/hooks/
├── pre-commit          # 提交前检查
├── commit-msg         # 提交信息规范
├── pre-push           # 推送前检查
├── post-commit        # 提交后通知
├── post-merge         # 合并后执行
└── pre-rebase         # 变基前检查
```

## 预定义 Hooks

### pre-commit (提交前检查)

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 正在执行提交前检查..."

# 检查代码格式
if [ -f "package.json" ]; then
  npm run lint --silent 2>/dev/null
  if [ $? -ne 0 ]; then
    echo "❌ Lint 检查失败，请修复后重试"
    exit 1
  fi
fi

# 检查测试
if [ -f "package.json" ]; then
  npm test --silent 2>/dev/null
  if [ $? -ne 0 ]; then
    echo "❌ 测试失败，请修复后重试"
    exit 1
  fi
fi

# 检查敏感信息
if git diff --cached | grep -E "(api_key|password|secret|token)" &>/dev/null; then
  echo "⚠️  检测到可能的敏感信息，请确认是否安全"
fi

echo "✅ 提交前检查通过"
```

### commit-msg (提交信息规范)

```bash
#!/bin/bash
# .git/hooks/commit-msg

COMMIT_MSG=$(cat "$1")

# 至少 10 个字符
if [ ${#COMMIT_MSG} -lt 10 ]; then
  echo "❌ 提交信息过短，至少需要 10 个字符"
  exit 1
fi

# 推荐格式检查
PATTERN="^(feat|fix|docs|style|refactor|perf|test|chore)(\(.+\))?: .{1,50}"
if ! echo "$COMMIT_MSG" | grep -qE "$PATTERN"; then
  echo "⚠️  建议格式: <type>(<scope>): <description>"
  echo "类型: feat, fix, docs, style, refactor, perf, test, chore"
fi

echo "✅ 提交信息检查完成"
```

### pre-push (推送前检查)

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "🚀 正在执行推送前检查..."

# 检查分支名称
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null)
if [[ "$CURRENT_BRANCH" =~ ^(main|master|dev)$ ]]; then
  read -p "⚠️  即将推送到保护分支，是否继续？(y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# 运行完整测试
if [ -f "package.json" ]; then
  echo "🧪 运行完整测试..."
  npm test 2>/dev/null
  if [ $? -ne 0 ]; then
    echo "❌ 测试失败，禁止推送"
    exit 1
  fi
fi

echo "✅ 推送前检查通过"
```

## 自动化安装

### 安装脚本

```bash
#!/bin/bash
# scripts/install-hooks.sh

HOOKS_DIR=".git/hooks"
TEMPLATE_DIR="hooks"

echo "📦 安装 Git hooks..."

# 创建 hooks 目录
mkdir -p "$HOOKS_DIR"

# 安装每个 hook
for hook in pre-commit commit-msg pre-push post-commit post-merge; do
  if [ -f "$TEMPLATE_DIR/$hook" ]; then
    cp "$TEMPLATE_DIR/$hook" "$HOOKS_DIR/$hook"
    chmod +x "$HOOKS_DIR/$hook"
    echo "✅ 安装 $hook"
  fi
done

echo "✨ Git hooks 安装完成!"
```

### Node.js Hook 管理器

```javascript
// scripts/hooks-manager.js

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const HOOKS_SOURCE = path.join(__dirname, '..', 'hooks');
const HOOKS_TARGET = path.join(process.cwd(), '.git', 'hooks');

const HOOKS = {
  'pre-commit': '#!/bin/bash\nnode scripts/pre-commit-hook.js',
  'commit-msg': '#!/bin/bash\nnode scripts/commit-msg-hook.js "$1"',
  'pre-push': '#!/bin/bash\nnode scripts/pre-push-hook.js',
};

function installHooks() {
  console.log('📦 安装 Git hooks...');

  if (!fs.existsSync(HOOKS_TARGET)) {
    fs.mkdirSync(HOOKS_TARGET, { recursive: true });
  }

  for (const [name, content] of Object.entries(HOOKS)) {
    const targetPath = path.join(HOOKS_TARGET, name);
    fs.writeFileSync(targetPath, content);
    fs.chmodSync(targetPath, '755');
    console.log(`✅ 安装 ${name}`);
  }

  console.log('✨ Git hooks 安装完成!');
}

function uninstallHooks() {
  console.log('🗑️  卸载 Git hooks...');

  for (const name of Object.keys(HOOKS)) {
    const targetPath = path.join(HOOKS_TARGET, name);
    if (fs.existsSync(targetPath)) {
      fs.unlinkSync(targetPath);
      console.log(`✅ 移除 ${name}`);
    }
  }

  console.log('✨ Git hooks 卸载完成!');
}

const command = process.argv[2];
if (command === 'uninstall') {
  uninstallHooks();
} else {
  installHooks();
}
```

## 与 AI 集成

### AI 辅助提交

```bash
#!/bin/bash
# hooks/ai-commit-helper.sh

echo "🤖 AI 提交助手"

# 获取 diff
CHANGES=$(git diff --cached --stat)
echo "变更内容:"
echo "$CHANGES"

# 调用 AI 生成提交信息
read -p "是否使用 AI 生成提交信息？(y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
  # 这里调用你的 AI 服务生成提交信息
  AI_MSG=$(node scripts/ai-commit-message.js)
  echo "AI 生成的提交信息:"
  echo "$AI_MSG"
  read -p "确认使用此提交信息？(y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "$AI_MSG" > .git/COMMIT_EDITMSG
  fi
fi
```

## 条件执行

### 仅在特定目录变更时触发

```bash
#!/bin/bash
# hooks/check-specific-files.sh

CHANGED_FILES=$(git diff --cached --name-only)
PATTERN="^src/"

if echo "$CHANGED_FILES" | grep -qE "$PATTERN"; then
  echo "📂 检测到 src 目录变更，运行检查..."
  npm run lint
  npm run test
else
  echo "ℹ️  未检测到 src 目录变更，跳过检查"
fi
```

### 跳过 Hooks

```bash
# 跳过单个 hook
git commit --no-verify -m "跳过 lint 检查"

# 跳过所有 hooks
git commit --no-hooks -m "紧急修复"
```
