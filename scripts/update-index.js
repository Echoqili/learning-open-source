#!/usr/bin/env node

/**
 * 更新 skills-index.json
 * 自动扫描所有 skills 并生成索引
 */

const fs = require('fs');
const path = require('path');

const SKILLS_DIR = 'd:\\pyworkplace\\github\\learning-open-source\\all-skills\\skills';
const OUTPUT_FILE = 'd:\\pyworkplace\\github\\learning-open-source\\skills-index.json';

function scanSkills(dir) {
  const skills = [];

  if (!fs.existsSync(dir)) {
    return skills;
  }

  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      const skillFile = path.join(fullPath, 'SKILL.md');
      if (fs.existsSync(skillFile)) {
        const skillData = parseSkillFile(skillFile, entry.name);
        skills.push(skillData);
      }
    }
  }

  return skills;
}

function parseSkillFile(filePath, name) {
  let content = '';
  try {
    content = fs.readFileSync(filePath, 'utf-8');
  } catch (e) {
    return { name, description: name, tags: [], difficulty: 'intermediate' };
  }

  let description = '';
  let tags = [];
  let difficulty = 'intermediate';

  const lines = content.split('\n');
  for (const line of lines) {
    if (line.startsWith('# ') && !description) {
      description = line.substring(2).trim();
    }
    if (line.includes('标签:') || line.includes('tags:')) {
      const tagMatch = line.match(/[\[【]?.+?[\]】]/g);
      if (tagMatch) {
        tags = tagMatch.map(t => t.replace(/[\[\]【】]/g, ''));
      }
    }
    if (line.includes('难度:') || line.includes('difficulty:')) {
      if (line.includes('初学者') || line.includes('beginner')) {
        difficulty = 'beginner';
      } else if (line.includes('高级') || line.includes('advanced')) {
        difficulty = 'advanced';
      }
    }
  }

  return {
    name,
    description: description || name,
    tags,
    difficulty,
    path: `all-skills/skills/${name}/SKILL.md`,
    created: new Date().toISOString().split('T')[0]
  };
}

function main() {
  console.log('🔍 扫描 Skills 目录...');

  const skills = scanSkills(SKILLS_DIR);

  const index = {
    version: '1.0',
    lastUpdated: new Date().toISOString(),
    total: skills.length,
    skills
  };

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(index, null, 2));

  console.log(`✅ 已更新 skills-index.json (${skills.length} skills)`);

  console.log('\n📦 新增的 Skills:');
  const newSkills = [
    'chinese-code-review',
    'chinese-git-workflow',
    'chinese-commit-conventions',
    'chinese-documentation',
    'executing-plans',
    'finishing-a-development-branch',
    'using-git-worktrees',
    'receiving-code-review',
    'requesting-code-review',
    'writing-skills',
    'using-superpowers',
    'brainstorming',
    'test-driven-development',
    'systematic-debugging',
    'subagent-driven-development',
    'mcp-builder',
    'verification-before-completion',
    'workflow-runner',
    'dispatching-parallel-agents',
    'writing-plans'
  ];

  const existingNames = skills.map(s => s.name);
  newSkills.forEach(s => {
    if (existingNames.includes(s)) {
      console.log(`  ✅ ${s}`);
    } else {
      console.log(`  ⬜ ${s} (未找到)`);
    }
  });
}

main();
