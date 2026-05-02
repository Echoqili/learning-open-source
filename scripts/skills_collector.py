#!/usr/bin/env python3
"""
高效 Skills 收集工作流
支持多数据源：GitHub Trending、DeepWiki、Zread、Awesome Lists
"""
import os
import sys
import json
import time
import requests
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv(Path(__file__).parent.parent / ".env")

PROJECT_ROOT = Path(__file__).parent.parent
CANDIDATES_FILE = PROJECT_ROOT / "candidates.json"
CACHE_FILE = PROJECT_ROOT / ".skills_cache.json"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY", "")
ZHIPU_API_URL = os.environ.get("ZHIPU_API_URL", "https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions")
ZHIPU_MODEL = os.environ.get("ZHIPU_MODEL", "kimi-k2.6")

GITHUB_HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
if GITHUB_TOKEN:
    GITHUB_HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

REQUEST_TIMEOUT = 60
MAX_RETRIES = 3
RETRY_DELAY = 2


def retry_request(url, headers=None, params=None, method="GET", json_data=None, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            if method == "GET":
                resp = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT, verify=True)
            else:
                resp = requests.post(url, headers=headers, json=json_data, timeout=REQUEST_TIMEOUT, verify=True)
            
            if resp.status_code in [200, 201]:
                return resp
            elif resp.status_code == 403:
                print(f"    Rate limited, waiting...")
                time.sleep(60)
            elif resp.status_code == 404:
                return None
        except requests.exceptions.SSLError:
            if attempt < max_retries - 1:
                print(f"    SSL error, retry {attempt+1}/{max_retries}")
                time.sleep(RETRY_DELAY * (attempt + 1))
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"    Timeout, retry {attempt+1}/{max_retries}")
                time.sleep(RETRY_DELAY)
        except requests.exceptions.ConnectionError as e:
            if attempt < max_retries - 1:
                print(f"    Connection error, retry {attempt+1}/{max_retries}")
                time.sleep(RETRY_DELAY * 2)
        except Exception as e:
            print(f"    Request error: {e}")
            break
    return None


@dataclass
class SkillCandidate:
    name: str
    full_name: str
    url: str
    stars: int
    description: str
    source: str
    category: str = "unknown"
    language: str = ""
    topics: List[str] = None
    
    def __post_init__(self):
        if self.topics is None:
            self.topics = []


class MultiSourceCollector:
    def __init__(self, min_stars: int = 100):
        self.min_stars = min_stars
        self.collected: List[SkillCandidate] = []
        self.seen_urls: Set[str] = set()
        
    def collect_all(self) -> List[SkillCandidate]:
        print("🚀 开始多源收集 Skills...")
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.collect_github_trending): "GitHub Trending",
                executor.submit(self.collect_awesome_lists): "Awesome Lists",
                executor.submit(self.collect_github_search): "GitHub Search",
                executor.submit(self.collect_deepwiki): "DeepWiki",
            }
            
            for future in as_completed(futures):
                source = futures[future]
                try:
                    results = future.result()
                    print(f"  ✅ {source}: {len(results)} candidates")
                except Exception as e:
                    print(f"  ❌ {source}: {e}")
        
        self._deduplicate()
        self._save_candidates()
        return self.collected
    
    def collect_github_trending(self) -> List[SkillCandidate]:
        results = []
        
        queries = [
            "claude skill",
            "cursor rule",
            "copilot instruction",
            "ai agent framework",
        ]
        
        for query in queries:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": f"{query} stars:>50",
                "per_page": 20,
                "sort": "stars",
                "order": "desc"
            }
            
            resp = retry_request(url, headers=GITHUB_HEADERS, params=params)
            if resp:
                for item in resp.json().get("items", []):
                    candidate = self._parse_repo(item, "github-trending")
                    if candidate and candidate.stars >= self.min_stars:
                        if candidate.url not in self.seen_urls:
                            self.seen_urls.add(candidate.url)
                            self.collected.append(candidate)
                            results.append(candidate)
            
            time.sleep(2)
        
        return results
    
    def collect_awesome_lists(self) -> List[SkillCandidate]:
        results = []
        
        known_skill_repos = [
            ("anthropics/anthropic-cookbook", "ai-product"),
            ("openai/openai-cookbook", "ai-product"),
            ("langchain-ai/langchain", "ai-product"),
            ("microsoft/semantic-kernel", "ai-product"),
            ("e2b-dev/awesome-ai-agents", "ai-product"),
            ("AgentOps-AI/awesome-ai-agents", "ai-product"),
            ("sindresorhus/awesome", "superpowers"),
            ("steven2358/awesome-generative-ai", "ai-product"),
            ("mahseema/awesome-ai-tools", "ai-product"),
            ("public-apis/public-apis", "dev-workflow"),
            ("kdeldycke/awesome-falsehood", "dev-quality"),
            ("analysis-tools-dev/static-analysis", "dev-quality"),
            ("enaqx/awesome-react", "dev-quality"),
            ("vuejs/awesome-vue", "dev-quality"),
            ("bradtraversy/design-resources-for-developers", "design"),
            ("ripienaar/free-for-dev", "dev-workflow"),
        ]
        
        for full_name, category in known_skill_repos:
            repo_data = self._get_repo_info(full_name)
            if repo_data:
                candidate = self._parse_repo(repo_data, "awesome-list")
                if candidate:
                    candidate.category = category
                    if candidate.url not in self.seen_urls:
                        self.seen_urls.add(candidate.url)
                        self.collected.append(candidate)
                        results.append(candidate)
            time.sleep(0.5)
        
        return results
    
    def collect_github_search(self) -> List[SkillCandidate]:
        results = []
        
        queries = [
            "claude-code skill",
            "cursor rules",
            "copilot instructions",
            "ai agent tools",
            "llm prompt engineering",
        ]
        
        for query in queries:
            url = "https://api.github.com/search/repositories"
            params = {"q": f"{query} stars:>50", "per_page": 15, "sort": "stars", "order": "desc"}
            
            resp = retry_request(url, headers=GITHUB_HEADERS, params=params)
            if resp:
                for item in resp.json().get("items", []):
                    candidate = self._parse_repo(item, "github-search")
                    if candidate and candidate.url not in self.seen_urls:
                        self.seen_urls.add(candidate.url)
                        self.collected.append(candidate)
                        results.append(candidate)
            
            time.sleep(2)
        
        return results
    
    def collect_deepwiki(self) -> List[SkillCandidate]:
        results = []
        
        trending_skills = [
            ("microsoft/playwright", "qa-testing"),
            ("puppeteer/puppeteer", "qa-testing"),
            ("nestjs/nest", "dev-workflow"),
            ("vercel/next.js", "dev-workflow"),
            ("tailwindlabs/tailwindcss", "design"),
            ("shadcn-ui/ui", "design"),
            ("prisma/prisma", "dev-workflow"),
            ("trpc/trpc", "dev-workflow"),
            ("vitest-dev/vitest", "qa-testing"),
            ("jestjs/jest", "qa-testing"),
        ]
        
        for full_name, category in trending_skills:
            repo_data = self._get_repo_info(full_name)
            if repo_data:
                candidate = self._parse_repo(repo_data, "deepwiki")
                if candidate:
                    candidate.category = category
                    if candidate.url not in self.seen_urls:
                        self.seen_urls.add(candidate.url)
                        self.collected.append(candidate)
                        results.append(candidate)
            time.sleep(0.5)
        
        return results
    
    def _get_repo_info(self, full_name: str) -> Optional[Dict]:
        url = f"https://api.github.com/repos/{full_name}"
        resp = retry_request(url, headers=GITHUB_HEADERS)
        if resp:
            return resp.json()
        return None
    
    def _parse_repo(self, item: Dict, source: str) -> Optional[SkillCandidate]:
        try:
            return SkillCandidate(
                name=item.get("name", ""),
                full_name=item.get("full_name", item.get("full_name", "")),
                url=item.get("html_url", f"https://github.com/{item.get('full_name', '')}"),
                stars=item.get("stargazers_count", item.get("stars", 0)),
                description=item.get("description", "") or "",
                source=source,
                language=item.get("language", "") or "",
                topics=item.get("topics", []) or []
            )
        except:
            return None
    
    def _deduplicate(self):
        unique = {}
        for c in self.collected:
            if c.full_name not in unique:
                unique[c.full_name] = c
        self.collected = list(unique.values())
        self.collected.sort(key=lambda x: x.stars, reverse=True)
    
    def _save_candidates(self):
        data = {
            "collected_at": datetime.now().isoformat(),
            "total": len(self.collected),
            "candidates": [asdict(c) for c in self.collected]
        }
        with open(CANDIDATES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n💾 已保存 {len(self.collected)} 个候选到 {CANDIDATES_FILE}")


def classify_with_ai(candidates: List[SkillCandidate], top_k: int = 20) -> List[Dict]:
    if not ZHIPU_API_KEY:
        print("⚠️ ZHIPU_API_KEY 未配置，跳过 AI 分类")
        return []
    
    print(f"\n🤖 AI 分类 Top {top_k} 候选...")
    
    top_candidates = candidates[:top_k]
    candidate_list = "\n".join([
        f"- {c.full_name} ({c.stars}⭐): {c.description[:80]}"
        for c in top_candidates
    ])
    
    prompt = f"""分析以下 GitHub 仓库，判断哪些是 Claude/Cursor/AI 相关的 Skills 或 Rules 项目。

候选仓库：
{candidate_list}

请返回 JSON 数组，格式：
[{{"full_name": "owner/repo", "is_skill": true/false, "category": "dev-workflow/design/ai-product/superpowers/qa-testing", "reason": "简短理由"}}]

只返回 JSON，不要其他文字。"""

    try:
        resp = requests.post(
            ZHIPU_API_URL,
            headers={
                "Authorization": f"Bearer {ZHIPU_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": ZHIPU_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 4000,
                "thinking": {"type": "disabled"}
            },
            timeout=60
        )
        
        if resp.status_code == 200:
            content = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            match = re.search(r'\[.*\]', content, re.DOTALL)
            if match:
                return json.loads(match.group())
    except Exception as e:
        print(f"AI 分类错误: {e}")
    
    return []


def main():
    import argparse
    parser = argparse.ArgumentParser(description="高效 Skills 收集工作流")
    parser.add_argument("--min-stars", type=int, default=100, help="最小 stars 数")
    parser.add_argument("--classify", action="store_true", help="使用 AI 分类")
    parser.add_argument("--top-k", type=int, default=20, help="AI 分类数量")
    
    args = parser.parse_args()
    
    collector = MultiSourceCollector(min_stars=args.min_stars)
    candidates = collector.collect_all()
    
    print(f"\n📊 收集统计:")
    print(f"  总计: {len(candidates)} 个候选")
    
    by_source = {}
    for c in candidates:
        by_source[c.source] = by_source.get(c.source, 0) + 1
    for source, count in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f"  {source}: {count}")
    
    print(f"\n🏆 Top 10 Stars:")
    for i, c in enumerate(candidates[:10], 1):
        print(f"  {i}. {c.full_name} ({c.stars:,}⭐)")
        print(f"     {c.description[:60]}...")
    
    if args.classify and candidates:
        classifications = classify_with_ai(candidates, args.top_k)
        if classifications:
            print(f"\n✅ AI 分类结果:")
            skill_count = sum(1 for c in classifications if c.get("is_skill"))
            print(f"  Skills: {skill_count}/{len(classifications)}")
            
            for c in classifications:
                if c.get("is_skill"):
                    print(f"  ✅ {c['full_name']} -> {c.get('category', 'unknown')}")
                    print(f"     {c.get('reason', '')}")


if __name__ == "__main__":
    main()
