#!/usr/bin/env python3
"""
GitHub Skills Scanner - 定期扫描 GitHub 上的优秀 Skills 项目
自动发现新的 skills 源，并按质量评分排序
"""

import os
import json
import re
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Skills-Scanner/1.0"
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

SKILLS_ROOT = Path(__file__).parent.parent
SCAN_RESULTS = SKILLS_ROOT / "scan-results.json"
POPULAR_SKILLS_FILE = SKILLS_ROOT / "popular-skills.md"

SEARCH_QUERIES = [
    "claude code skills site:github.com",
    "cursor skills site:github.com",
    "agent skills AI site:github.com",
    "SKILL.md prompts site:github.com",
    "claude subagent site:github.com",
    "openclaw skills site:github.com",
]

QUALITY_PATTERNS = {
    "has_skill_md": r"SKILL\.md",
    "has_readme": r"README\.md",
    "has_examples": r"(example|sample)",
    "has_docs": r"(docs?|documentation)",
    "professional_structure": r"(skills?|agents?|prompts?)/",
}

STAR_THRESHOLDS = {
    "excellent": 1000,
    "good": 500,
    "average": 100,
}


def search_github(query: str, per_page: int = 30) -> List[Dict]:
    """搜索 GitHub 仓库"""
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "per_page": per_page, "sort": "stars", "order": "desc"}

    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        if resp.status_code == 200:
            return resp.json().get("items", [])
        elif resp.status_code == 403:
            print(f"⚠️ Rate limited, waiting...")
            return []
        else:
            print(f"❌ Search failed: {resp.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def get_repo_details(owner: str, repo: str) -> Dict:
    """获取仓库详细信息"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        return {}
    except:
        return {}


def check_skill_md_exists(owner: str, repo: str) -> bool:
    """检查仓库是否包含 SKILL.md"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/SKILL.md"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        return resp.status_code == 200
    except:
        return False


def count_skills_in_repo(owner: str, repo: str) -> int:
    """统计仓库中的 skills 数量"""
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            tree = resp.json().get("tree", [])
            skill_count = sum(1 for item in tree if "SKILL.md" in item.get("path", ""))
            return skill_count
        return 0
    except:
        return 0


def analyze_quality(repo_data: Dict) -> Dict:
    """分析仓库质量"""
    score = 0
    factors = {}

    stars = repo_data.get("stargazers_count", 0)
    if stars >= STAR_THRESHOLDS["excellent"]:
        score += 50
    elif stars >= STAR_THRESHOLDS["good"]:
        score += 30
    elif stars >= STAR_THRESHOLDS["average"]:
        score += 10

    factors["stars"] = stars

    has_wiki = repo_data.get("has_wiki", False)
    if has_wiki:
        score += 5
    factors["has_wiki"] = has_wiki

    has_issues = repo_data.get("has_issues", False)
    if has_issues:
        score += 3
    factors["has_issues"] = has_issues

    topics = repo_data.get("topics", [])
    if any(t in topics for t in ["skills", "claude", "cursor", "agent", "prompts"]):
        score += 15
    factors["topics"] = topics

    language = repo_data.get("language", "")
    if language in ["Python", "TypeScript", "JavaScript", "Shell"]:
        score += 5
    factors["language"] = language

    description = repo_data.get("description", "") or ""
    if "skill" in description.lower():
        score += 10
    factors["description_length"] = len(description)

    return {
        "score": score,
        "factors": factors,
        "rating": "excellent" if score >= 50 else "good" if score >= 30 else "average"
    }


def scan_popular_skills() -> List[Dict]:
    """扫描热门 skills"""
    print("🔍 扫描 GitHub 热门 Skills...")

    all_repos = []
    seen = set()

    for query in SEARCH_QUERIES:
        print(f"📡 搜索: {query[:50]}...")
        repos = search_github(query)

        for repo in repos:
            full_name = repo.get("full_name", "")
            if full_name and full_name not in seen:
                seen.add(full_name)
                all_repos.append(repo)

        if len(all_repos) >= 200:
            break

    results = []
    for repo in all_repos[:100]:
        owner, name = repo["full_name"].split("/", 1)
        details = get_repo_details(owner, name)
        skill_count = count_skills_in_repo(owner, name)

        if skill_count > 0 or check_skill_md_exists(owner, name):
            quality = analyze_quality(details)
            results.append({
                "owner": owner,
                "repo": name,
                "full_name": repo["full_name"],
                "description": repo.get("description", ""),
                "stars": repo.get("stargazers_count", 0),
                "language": repo.get("language", ""),
                "skills_count": skill_count,
                "quality": quality,
                "url": repo.get("html_url", ""),
                "topics": repo.get("topics", []),
                "updated_at": repo.get("updated_at", "")
            })

    results.sort(key=lambda x: (-x["stars"], -x["quality"]["score"]))

    scan_data = {
        "scanned_at": datetime.now().isoformat(),
        "total_found": len(results),
        "repositories": results[:50]
    }

    SCAN_RESULTS.write_text(json.dumps(scan_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✅ 扫描完成，发现 {len(results)} 个 Skills 仓库")

    return results


def generate_popular_readme(results: List[Dict]) -> str:
    """生成热门 Skills README"""
    lines = [
        "# Popular AI Skills Repositories",
        "",
        f"> 扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> 发现仓库: {len(results)}",
        "",
        "---\n",
        "",
        "## ⭐ Top 50 Skills Repositories",
        "",
        "| Rank | Repository | Stars | Quality | Skills | Description |",
        "|------|------------|-------|---------|--------|-------------|"
    ]

    for i, repo in enumerate(results[:50], 1):
        quality_badge = {
            "excellent": "🟢 Excellent",
            "good": "🟡 Good",
            "average": "⚪ Average"
        }.get(repo["quality"]["rating"], "⚪")

        desc = (repo.get("description") or "")[:50]
        if len(repo.get("description") or "") > 50:
            desc += "..."

        lines.append(
            f"| {i} | [{repo['full_name']}]({repo['url']}) "
            f"| {repo['stars']:,} | {quality_badge} "
            f"| {repo['skills_count']} | {desc} |"
        )

    lines.extend([
        "",
        "## 📊 分类统计",
        ""
    ])

    by_lang = {}
    for repo in results:
        lang = repo.get("language") or "Unknown"
        if lang not in by_lang:
            by_lang[lang] = []
        by_lang[lang].append(repo)

    for lang, repos in sorted(by_lang.items(), key=lambda x: -len(x[1]))[:10]:
        lines.append(f"### {lang} ({len(repos)})")
        lines.append("")
        for repo in repos[:5]:
            lines.append(f"- [{repo['full_name']}]({repo['url']}) ⭐{repo['stars']}")
        lines.append("")

    lines.extend([
        "---\n",
        "*此文件由脚本自动生成，定期扫描 GitHub 上的热门 Skills 仓库*\n"
    ])

    return '\n'.join(lines)


def main():
    print("🚀 GitHub Skills Scanner")
    print("=" * 40)

    if not GITHUB_TOKEN:
        print("⚠️ 未设置 GITHUB_TOKEN，搜索可能受限")

    results = scan_popular_skills()

    print("\n📝 生成热门 Skills 文档...")
    readme = generate_popular_readme(results)
    POPULAR_SKILLS_FILE.write_text(readme, encoding='utf-8')
    print(f"✅ 已保存到 {POPULAR_SKILLS_FILE}")

    print("\n🏆 Top 10 热门仓库:")
    for i, repo in enumerate(results[:10], 1):
        print(f"  {i}. {repo['full_name']} ⭐{repo['stars']:,} ({repo['skills_count']} skills)")


if __name__ == "__main__":
    main()
