#!/usr/bin/env node

/**
 * Superpowers-zh 安装脚本
 * 一键安装 AI 编程助手技能到主流 IDE
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SUPPORTED_TOOLS = {
  'claude': {
    name: 'Claude Code',
    configDir: '~/.claude',
    skillsDir: '.skills',
    installCommand: 'claude skills install'
  },
  'cursor': {
    name: 'Cursor',
    configDir: '~/.cursor',
    skillsDir: 'skills',
    installCommand: null
  },
  'windsurf': {
    name: 'Windsurf',
    configDir: '~/.windsurf',
    skillsDir: 'skills',
    installCommand: null
  },
  'kiro': {
    name: 'Kiro',
    configDir: '~/.kiro',
    skillsDir: 'skills',
    installCommand: null
  }
};

const SOURCE_DIR = path.join(__dirname, '..', 'all-skills', 'skills');

function log(message, type = 'info') {
  const prefix = {
    info: 'ℹ️ ',
    success: '✅',
    error: '❌',
    warning: '⚠️'
  };
  console.log(`${prefix[type]} ${message}`);
}

function detectInstalledTools() {
  const installed = [];
  for (const [key, tool] of Object.entries(SUPPORTED_TOOLS)) {
    try {
      const configPath = path.expandHome(configDir);
      if (fs.existsSync(configPath)) {
        installed.push(key);
      }
    } catch (e) {
      // Tool not installed
    }
  }
  return installed;
}

function getSkillsList() {
  if (!fs.existsSync(SOURCE_DIR)) {
    return [];
  }
  return fs.readdirSync(SOURCE_DIR).filter(f => {
    return fs.statSync(path.join(SOURCE_DIR, f)).isDirectory();
  });
}

function installToClaude(skills) {
  const configDir = path.expandHome(SUPPORTED_TOOLS.claude.configDir);
  const skillsDir = path.join(configDir, SUPPORTED_TOOLS.claude.skillsDir);

  log(`安装到 Claude Code...`);

  // Create skills directory
  if (!fs.existsSync(skillsDir)) {
    fs.mkdirSync(skillsDir, { recursive: true });
  }

  // Copy skills
  let installed = 0;
  for (const skill of skills) {
    const src = path.join(SOURCE_DIR, skill);
    const dest = path.join(skillsDir, skill);

    if (fs.existsSync(src)) {
      copyDirectory(src, dest);
      installed++;
      log(`已安装: ${skill}`);
    }
  }

  log(`Claude Code 安装完成 (${installed} 个技能)`);
}

function installToCursor(skills) {
  const configDir = path.expandHome(SUPPORTED_TOOLS.cursor.configDir);
  const skillsDir = path.join(configDir, SUPPORTED_TOOLS.cursor.skillsDir);

  log(`安装到 Cursor...`);

  if (!fs.existsSync(skillsDir)) {
    fs.mkdirSync(skillsDir, { recursive: true });
  }

  let installed = 0;
  for (const skill of skills) {
    const src = path.join(SOURCE_DIR, skill);
    const dest = path.join(skillsDir, skill);

    if (fs.existsSync(src)) {
      copyDirectory(src, dest);
      installed++;
    }
  }

  log(`Cursor 安装完成 (${installed} 个技能)`);
}

function installToWindsurf(skills) {
  const configDir = path.expandHome(SUPPORTED_TOOLS.windsurf.configDir);
  const skillsDir = path.join(configDir, SUPPORTED_TOOLS.windsurf.skillsDir);

  log(`安装到 Windsurf...`);

  if (!fs.existsSync(skillsDir)) {
    fs.mkdirSync(skillsDir, { recursive: true });
  }

  let installed = 0;
  for (const skill of skills) {
    const src = path.join(SOURCE_DIR, skill);
    const dest = path.join(skillsDir, skill);

    if (fs.existsSync(src)) {
      copyDirectory(src, dest);
      installed++;
    }
  }

  log(`Windsurf 安装完成 (${installed} 个技能)`);
}

function installToKiro(skills) {
  const configDir = path.expandHome(SUPPORTED_TOOLS.kiro.configDir);
  const skillsDir = path.join(configDir, SUPPORTED_TOOLS.kiro.skillsDir);

  log(`安装到 Kiro...`);

  if (!fs.existsSync(skillsDir)) {
    fs.mkdirSync(skillsDir, { recursive: true });
  }

  let installed = 0;
  for (const skill of skills) {
    const src = path.join(SOURCE_DIR, skill);
    const dest = path.join(skillsDir, skill);

    if (fs.existsSync(src)) {
      copyDirectory(src, dest);
      installed++;
    }
  }

  log(`Kiro 安装完成 (${installed} 个技能)`);
}

function copyDirectory(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDirectory(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function createGitHooks() {
  const hooksDir = path.join('.git', 'hooks');
  if (!fs.existsSync(hooksDir)) {
    fs.mkdirSync(hooksDir, { recursive: true });
  }

  const preCommitHook = `#!/bin/sh
# Superpowers-zh pre-commit hook
# 自动代码审查

echo "🔍 运行提交前检查..."

# 检查是否有未解决的审查意见
if grep -q "TODO.*review" $(git diff --cached --name-only); then
  echo "⚠️  存在未完成的审查 TODO"
fi

# 运行 lint
if [ -f "package.json" ]; then
  npm run lint --silent 2>/dev/null
fi

echo "✅ 提交前检查完成"
`;

  const commitMsgHook = `#!/bin/sh
# Superpowers-zh commit-msg hook
# 规范提交信息

COMMIT_MSG=$(cat "$1")
PATTERN="^(feat|fix|docs|style|refactor|perf|test|chore)(\\(.+\\))?: .{1,50}"

if ! echo "$COMMIT_MSG" | grep -qE "$PATTERN"; then
  echo "❌ 提交信息格式不规范"
  echo "格式: <type>(<scope>): <description>"
  echo "类型: feat, fix, docs, style, refactor, perf, test, chore"
  exit 1
fi

echo "✅ 提交信息格式正确"
`;

  fs.writeFileSync(path.join(hooksDir, 'pre-commit'), preCommitHook);
  fs.writeFileSync(path.join(hooksDir, 'commit-msg'), commitMsgHook);

  fs.chmodSync(path.join(hooksDir, 'pre-commit'), '755');
  fs.chmodSync(path.join(hooksDir, 'commit-msg'), '755');

  log('Git hooks 已创建');
}

function printHelp() {
  console.log(`
Superpowers-zh 安装脚本

用法:
  node bin/superpowers-zh.js [选项]

选项:
  --all           安装到所有支持的工具
  --claude        安装到 Claude Code
  --cursor        安装到 Cursor
  --windsurf      安装到 Windsurf
  --kiro          安装到 Kiro
  --hooks         仅创建 Git hooks
  --list          列出所有可用技能
  --help          显示帮助

示例:
  node bin/superpowers-zh.js --all
  node bin/superpowers-zh.js --claude --list
  node bin/superpowers-zh.js --hooks
  `);
}

function main() {
  const args = process.argv.slice(2);

  if (args.includes('--help')) {
    printHelp();
    return;
  }

  if (args.includes('--list')) {
    const skills = getSkillsList();
    console.log('\n📦 可用技能列表:\n');
    skills.forEach(skill => {
      console.log(`  • ${skill}`);
    });
    console.log(`\n共 ${skills.length} 个技能\n`);
    return;
  }

  const skills = getSkillsList();
  console.log(`\n🚀 Superpowers-zh 安装器`);
  console.log(`📂 源目录: ${SOURCE_DIR}`);
  console.log(`📦 发现 ${skills.length} 个技能\n`);

  if (args.length === 0 || args.includes('--all')) {
    installToClaude(skills);
    installToCursor(skills);
    installToWindsurf(skills);
    installToKiro(skills);
  }

  if (args.includes('--claude')) installToClaude(skills);
  if (args.includes('--cursor')) installToCursor(skills);
  if (args.includes('--windsurf')) installToWindsurf(skills);
  if (args.includes('--kiro')) installToKiro(skills);

  if (args.includes('--hooks')) {
    createGitHooks();
  }

  if (args.length === 0) {
    createGitHooks();
  }

  console.log('\n✨ 安装完成!\n');
}

main();
