#!/usr/bin/env python3
"""
精确解析 PDF skills 列表
规律：URL 行前面的那行或同行包含 "作者 slug"
"""
import re
import json
from pathlib import Path

REPO_ROOT = Path("d:/pyworkplace/github/learning-open-source")

with open(REPO_ROOT / "pdf_all.txt", encoding="utf-8") as f:
    lines = f.readlines()
lines = [l.rstrip("\n") for l in lines]

# 加载现有 skills
with open(REPO_ROOT / "skills-index.json", encoding="utf-8") as f:
    idx = json.load(f)
existing_slugs = set()
for cat, info in idx["by_category"].items():
    for s in info["skills"]:
        existing_slugs.add(s["name"].lower().strip())

print(f"现有 skills: {len(existing_slugs)}")

# -------- 解析策略 --------
# 每条记录的关键信息全在 URL 行 ± 2 行内
# 格式变体：
#   A. "author slug https://clawhub.ai/..."    （同行）
#   B. "author slug-part1"  \n  "slug-part2"  \n  "https://..."  （跨行）
#   C. "https://clawhub.ai/author/"  只有URL（slug 在上一行）

records = {}  # slug -> record

for i, line in enumerate(lines):
    if "clawhub.ai" not in line:
        continue

    # ---- 提取完整 URL（可能跨行截断）----
    url_raw = re.search(r"https://clawhub\.ai/\S*", line)
    if not url_raw:
        continue
    url_part = url_raw.group(0)

    # URL 可能截断，取下一行补全
    if i + 1 < len(lines):
        next_line = lines[i + 1].strip()
        # 如果下一行是续接（不含空格、不以数字开头、不是新记录）
        if (next_line
                and not next_line.startswith("序号")
                and not re.match(r"^\d+\s", next_line)
                and "clawhub.ai" not in next_line
                and len(next_line) < 40
                and " " not in next_line
                and not next_line.startswith("•")):
            url_part = url_part.rstrip("/") + next_line

    # 提取 slug：URL 结构是 clawhub.ai/author/slug 或 clawhub.ai/slug
    url_path = url_part.replace("https://clawhub.ai/", "").rstrip("/")
    parts = url_path.split("/")
    slug = parts[-1] if parts else ""

    # 清理 slug：去掉截断的尾巴
    slug = re.sub(r"[^a-z0-9\-].*$", "", slug.lower())
    if not slug or len(slug) < 3:
        continue
    if not re.match(r"^[a-z][a-z0-9\-]+$", slug):
        continue

    # ---- 从同行提取 author ----
    # 格式：author slug URL  或  URL only
    before_url = line[:url_raw.start()].strip()
    author = ""
    if before_url:
        # author slug 可能在 URL 前
        tokens = before_url.split()
        if tokens:
            author = tokens[0]

    # ---- 向上找描述（最多8行）----
    desc_lines = []
    for j in range(max(0, i - 8), i):
        ln = lines[j].strip()
        if not ln:
            continue
        if ln.startswith("序号") or ln.startswith("•"):
            continue
        if re.match(r"^\d+\s+[A-Za-z]", ln):
            # 找到序号行，提取描述的开始
            # 格式：N  技能名称  技能描述...
            desc_match = re.match(r"^\d+\s+\S+\s+(.*)", ln)
            if desc_match:
                desc_lines = [desc_match.group(1)]
            else:
                desc_lines = []
        elif re.match(r"^\d+\s+[\u4e00-\u9fff]", ln):
            desc_start = re.match(r"^\d+\s+(.*)", ln)
            if desc_start:
                desc_lines = [desc_start.group(1)]
        elif desc_lines:
            desc_lines.append(ln)

    desc = " ".join(desc_lines).strip()
    # 清理：去掉作者名、slug 等残留
    desc = re.sub(r"\b[A-Za-z0-9_\-]+\s+[a-z][a-z0-9\-]+\s*$", "", desc).strip()

    # ---- 确定名称：slug 转可读格式 ----
    name_display = slug.replace("-", " ").title()

    if slug not in records:
        records[slug] = {
            "slug": slug,
            "name": name_display,
            "author": author,
            "desc": desc,
            "url": f"https://clawhub.ai/{url_path}",
        }

all_records = list(records.values())
print(f"解析到 unique slugs: {len(all_records)}")

# -------- 过滤：去掉现有的 --------
new_records = [r for r in all_records if r["slug"] not in existing_slugs]
print(f"去除现有后: {len(new_records)}")

# -------- 质量评分 --------
# 高价值 slug 关键词
HIGH_VALUE_SLUGS = {
    # 搜索/信息检索
    "tavily", "brave", "perplexity", "bing", "baidu", "google", "web-search",
    "search", "news", "research",
    # 开发工具
    "github", "gitlab", "git", "jira", "linear", "notion", "obsidian",
    "sqlite", "database", "redis", "docker", "kubernetes", "terraform",
    "vscode", "terminal", "shell", "cli", "api", "rest", "graphql",
    # AI/LLM 工具
    "llm", "openai", "anthropic", "gemini", "grok", "ollama", "rag",
    "embedding", "prompt", "agent", "whisper", "tts", "asr",
    # 生产力
    "email", "calendar", "slack", "telegram", "discord", "whatsapp",
    "todoist", "trello", "asana", "n8n", "zapier",
    # 数据分析
    "excel", "csv", "pandas", "sql", "analytics", "dashboard", "chart",
    "bigquery", "snowflake", "tableau", "powerbi",
    # 内容/媒体
    "youtube", "twitter", "linkedin", "reddit", "rss",
    "image", "video", "audio", "ocr", "pdf", "markdown",
    # 金融
    "stock", "crypto", "finance", "trading",
    # 安全
    "security", "pentest", "audit", "vulnerability",
    # 特色
    "feishu", "wechat", "dingtalk", "lark",
}

LOW_VALUE_PATTERNS = [
    r"^test-?\d*$",
    r"^skill-\d+$",
    r"^agent-\d+$",
    r"^demo",
    r"^example",
    r"^my-",
    r"^hello",
    r"^test-agent",
]

HIGH_VALUE_DESC_KW = [
    "搜索", "分析", "自动", "生成", "代码", "测试", "部署", "监控", "审计",
    "翻译", "总结", "研究", "数据", "图片", "视频", "API", "集成",
    "github", "notion", "jira", "slack", "email", "calendar",
    "search", "automat", "analyt", "deploy", "monitor", "generat",
    "research", "workflow", "integrat", "optimize",
]

def score_record(r):
    s = 0
    slug = r["slug"].lower()
    desc = r["desc"].lower()

    # slug 包含高价值词
    for kw in HIGH_VALUE_SLUGS:
        if kw in slug:
            s += 3
            break

    # desc 关键词
    for kw in HIGH_VALUE_DESC_KW:
        if kw.lower() in desc:
            s += 1

    # desc 长度奖励
    if len(r["desc"]) > 50:
        s += 2
    if len(r["desc"]) > 100:
        s += 1

    # 低质量惩罚
    for pat in LOW_VALUE_PATTERNS:
        if re.match(pat, slug):
            s -= 10
            break

    # slug 太短或太长
    if len(slug) < 4:
        s -= 5
    if len(slug) > 50:
        s -= 3

    # 纯截断的 slug（末尾是-）
    if slug.endswith("-"):
        s -= 5

    return s

for r in new_records:
    r["score"] = score_record(r)

new_records.sort(key=lambda x: -x["score"])

# 过滤掉负分
positive = [r for r in new_records if r["score"] >= 2]
print(f"质量过滤后（score>=2）: {len(positive)}")

# 保存
with open(REPO_ROOT / "pdf_candidates.json", "w", encoding="utf-8") as f:
    json.dump(positive[:200], f, ensure_ascii=False, indent=2)

print("\n=== TOP 80 精选 ===")
for r in positive[:80]:
    print(f"  [{r['score']:2d}] {r['slug']:45s} | {r['desc'][:70]}")
