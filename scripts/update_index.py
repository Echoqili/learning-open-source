#!/usr/bin/env python3
"""更新 skills-index.json，把新创建的 skills 加入索引"""
import json
import re
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path("d:/pyworkplace/github/learning-open-source")
INDEX_FILE = REPO_ROOT / "skills-index.json"
ALL_SKILLS_DIR = REPO_ROOT / "all-skills" / "skills"

# 新 skills 的分类映射
NEW_SKILLS_CATEGORIES = {
    "tavily-search":         ("superpowers", "Superpowers"),
    "web-search-pro":        ("superpowers", "Superpowers"),
    "deep-research":         ("superpowers", "Superpowers"),
    "github-api":            ("dev-workflow", "Dev Workflow"),
    "git-commit-automation": ("dev-workflow", "Dev Workflow"),
    "copilot-cli":           ("dev-workflow", "Dev Workflow"),
    "security-audit-toolkit":("dev-workflow", "Dev Workflow"),
    "web-deploy-github":     ("dev-workflow", "Dev Workflow"),
    "n8n-workflow":          ("dev-workflow", "Dev Workflow"),
    "sqlite-agent":          ("dev-workflow", "Dev Workflow"),
    "prompt-optimizer":      ("ai-product", "AI Product"),
    "rag-search":            ("ai-product", "AI Product"),
    "ai-code-review":        ("ai-product", "AI Product"),
    "bilibili-analytics":    ("superpowers", "Superpowers"),
    "google-search-console": ("superpowers", "Superpowers"),
    "excel-analyzer":        ("superpowers", "Superpowers"),
    "notion-api":            ("superpowers", "Superpowers"),
    "jira-skill":            ("dev-workflow", "Dev Workflow"),
    "todoist-api":           ("superpowers", "Superpowers"),
    "slack-api":             ("superpowers", "Superpowers"),
    "youtube-analytics":     ("superpowers", "Superpowers"),
    "wechat-publisher":      ("superpowers", "Superpowers"),
    "feishu-bitable-api":    ("superpowers", "Superpowers"),
    "baidu-search":          ("superpowers", "Superpowers"),
    "changelog-generator":   ("dev-workflow", "Dev Workflow"),
    "pentest-skill":         ("dev-workflow", "Dev Workflow"),
    "imap-email":            ("superpowers", "Superpowers"),
    "stock-analysis":        ("superpowers", "Superpowers"),
    "linkedin-lead-gen":     ("superpowers", "Superpowers"),
    "ga4-analytics":         ("superpowers", "Superpowers"),
    "apify-scraper":         ("superpowers", "Superpowers"),
}

# 加载现有索引
with open(INDEX_FILE, encoding="utf-8") as f:
    idx = json.load(f)

existing_by_name = {}
for cat, info in idx["by_category"].items():
    for s in info["skills"]:
        existing_by_name[s["name"]] = cat

added = 0
for slug, (cat_key, cat_name) in NEW_SKILLS_CATEGORIES.items():
    if slug in existing_by_name:
        continue

    skill_file = ALL_SKILLS_DIR / slug / "SKILL.md"
    if not skill_file.exists():
        print(f"  [SKIP] SKILL.md not found: {slug}")
        continue

    # 读取描述
    content = skill_file.read_text(encoding="utf-8")
    desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
    desc = desc_match.group(1).strip() if desc_match else ""

    # 确保分类存在
    if cat_key not in idx["by_category"]:
        idx["by_category"][cat_key] = {
            "name": cat_name,
            "description": f"{cat_name} skills",
            "color": "⚡",
            "skills": []
        }

    entry = {
        "name": slug,
        "path": f"all-skills\\skills\\{slug}\\SKILL.md",
        "description": desc,
        "purpose": desc,
        "source": "clawhub"
    }
    idx["by_category"][cat_key]["skills"].append(entry)
    added += 1
    print(f"  [+] {slug} -> {cat_key}")

# 重新统计 total_count
total = sum(len(info["skills"]) for info in idx["by_category"].values())
idx["total_count"] = total
idx["generated_at"] = datetime.now().isoformat()

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    json.dump(idx, f, ensure_ascii=False, indent=2)

print(f"\n索引更新完成: +{added} skills, total={total}")
