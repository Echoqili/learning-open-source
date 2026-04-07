#!/usr/bin/env python3
"""
Smart Skills Finder - 智能 Skills 搜索引擎
根据需求、使用场景、关键词快速找到合适的 Skills
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class SearchMode(Enum):
    KEYWORD = "keyword"
    SEMANTIC = "semantic"
    SCENARIO = "scenario"
    CATEGORY = "category"

@dataclass
class SearchResult:
    skill: Dict
    score: float
    match_reasons: List[str]
    category: str
    category_emoji: str

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"

CATEGORIES_EMOJI = {
    "product": "🔵",
    "agile": "🟢",
    "scrum": "🟡",
    "ddd": "🟠",
    "dev-quality": "🟣",
    "qa-testing": "🔴",
    "api-design": "⚪",
    "ai-product": "🩵",
    "ai-safety": "🚨",
    "superpowers": "⚡",
    "dev-workflow": "🔧",
    "design": "🎨",
    "skill-authoring": "🛠️",
    "indie-hacker": "💰",
}

SCENARIO_TEMPLATES = {
    "pm_basics": {
        "name": "产品经理基础",
        "emoji": "📋",
        "keywords": ["需求", "PRD", "用户故事", "用户研究", "产品规划", "roadmap"],
        "recommended": ["discovery-process", "user-story", "prd-development", "prioritization-advisor", "product-strategy-session"]
    },
    "pm_advanced": {
        "name": "高级产品经理",
        "emoji": "🎯",
        "keywords": ["战略", "路线图", "指标", "商业化", "增长", "CEO对话"],
        "recommended": ["business-health-diagnostic", "saas-economics-efficiency-metrics", "executive-onboarding-playbook", "altitude-horizon-framework"]
    },
    "customer_discovery": {
        "name": "客户探索与验证",
        "emoji": "🔍",
        "keywords": ["客户访谈", "发现", "验证", "用户研究", "访谈准备"],
        "recommended": ["discovery-interview-prep", "discovery-process", "customer-journey-map", "problem-statement", "jobs-to-be-done"]
    },
    "agile_dev": {
        "name": "敏捷开发团队",
        "emoji": "🏃",
        "keywords": ["敏捷", "Sprint", "规划", "回顾", "待办事项", "冲刺"],
        "recommended": ["sprint-planning", "backlog-refinement", "retrospective", "definition-of-done-enforcer", "sprint-goal-writer"]
    },
    "scrum_team": {
        "name": "Scrum团队",
        "emoji": "🎯",
        "keywords": ["Scrum", "仪式", "Scrum Master", "Product Owner"],
        "recommended": ["sprint-planning", "sprint-review", "retrospective", "backlog-refinement", "smoke-test"]
    },
    "qa_testing": {
        "name": "QA与测试",
        "emoji": "🧪",
        "keywords": ["测试", "质量", "自动化", "E2E", "Playwright", "单元测试"],
        "recommended": ["test-strategy", "playwright-automation", "e2e-testing", "unit-testing", "api-testing"]
    },
    "architecture": {
        "name": "架构设计",
        "emoji": "🏗️",
        "keywords": ["架构", "DDD", "领域模型", "六边形", "设计模式"],
        "recommended": ["ddd-skills", "api-generator"]
    },
    "dev_quality": {
        "name": "开发质量",
        "emoji": "💎",
        "keywords": ["代码质量", "重构", "调试", "Git", "整洁代码"],
        "recommended": ["clean-code", "debugger", "git-workflow", "coding-standards"]
    },
    "tdd_workflow": {
        "name": "TDD与测试驱动",
        "emoji": "⚡",
        "keywords": ["TDD", "测试驱动", "红绿重构", "单元测试"],
        "recommended": ["tdd-workflow", "test-driven-development", "systematic-debugging"]
    },
    "indie_hacker": {
        "name": "独立开发者创业",
        "emoji": "💰",
        "keywords": ["创业", "MVP", "冷启动", "获客", "增长", "变现"],
        "recommended": ["validate-idea", "mvp", "first-customers", "pricing", "marketing-plan", "grow-sustainably"]
    },
    "ai_product": {
        "name": "AI产品开发",
        "emoji": "🤖",
        "keywords": ["AI", "大模型", "Prompt", "幻觉", "安全"],
        "recommended": ["ai-product", "prompt-injection-defense", "hallucination-detection", "jailbreak-detection"]
    },
    "design_system": {
        "name": "设计系统",
        "emoji": "🎨",
        "keywords": ["设计", "UI", "UX", "组件", "设计令牌", "色板"],
        "recommended": ["design-system", "ui-ux-pro-max"]
    },
    "skill_creation": {
        "name": "Skill开发",
        "emoji": "🛠️",
        "keywords": ["Skill", "开发", "创建", "测试", "优化"],
        "recommended": ["skill-creator"]
    }
}

USAGE_EXAMPLES = [
    ("规划Sprint会议", "scrum_team"),
    ("写PRD文档", "pm_basics"),
    ("设计API架构", "architecture"),
    ("客户访谈准备", "customer_discovery"),
    ("搭建TDD流程", "tdd_workflow"),
    ("独立开发产品", "indie_hacker"),
    ("AI产品安全", "ai_product"),
    ("搭建设计系统", "design_system"),
]

class SmartSkillFinder:
    def __init__(self, index_path: Optional[Path] = None):
        if index_path is None:
            index_path = Path(__file__).parent.parent / "skills-index.json"
        self.index_path = index_path
        self.index = self._load_index()
        self._build_search_cache()

    def _load_index(self) -> Dict:
        if self.index_path.exists():
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _build_search_cache(self):
        self.all_skills = []
        self.skills_by_name = {}
        self.skills_by_category = {}

        self.cn_keywords_map = {
            "sprint": ["sprint", "冲刺", "迭代"],
            "planning": ["planning", "规划", "计划会议"],
            "backlog": ["backlog", "待办", "产品待办"],
            "retrospective": ["retrospective", "回顾", "复盘"],
            "review": ["review", "评审", "审查"],
            "user-story": ["user-story", "用户故事", "用户案例"],
            "prd": ["prd", "产品需求文档", "需求文档"],
            "roadmap": ["roadmap", "路线图", "产品路线图"],
            "test": ["test", "测试", "测验"],
            "tdd": ["tdd", "测试驱动", "红绿重构"],
            "api": ["api", "接口", "应用程序接口"],
            "design": ["design", "设计", "架构设计"],
            "debug": ["debug", "调试", "排错"],
            "clean-code": ["clean-code", "整洁代码", "代码质量"],
            "prompt": ["prompt", "提示词", "提示工程"],
            "injection": ["injection", "注入", "prompt注入"],
            "safety": ["safety", "安全", "安全测试"],
            "mvp": ["mvp", "最小可行产品", "原型"],
            "pricing": ["pricing", "定价", "价格策略"],
            "marketing": ["marketing", "营销", "市场推广"],
            "growth": ["growth", "增长", "用户增长"],
            "customer": ["customer", "客户", "用户"],
            "journey": ["journey", "旅程", "客户旅程"],
            "persona": ["persona", "画像", "用户画像"],
            "discovery": ["discovery", "发现", "探索"],
        }

        by_category = self.index.get("by_category", {})
        for cat_key, cat_info in by_category.items():
            emoji = CATEGORIES_EMOJI.get(cat_key, "⚪")
            self.skills_by_category[cat_key] = []

            for skill in cat_info.get("skills", []):
                skill_entry = {
                    **skill,
                    "category_key": cat_key,
                    "category_name": cat_info["name"],
                    "category_emoji": emoji,
                    "cn_keywords": self._extract_cn_keywords(skill)
                }
                self.all_skills.append(skill_entry)
                self.skills_by_name[skill["name"]] = skill_entry
                self.skills_by_category[cat_key].append(skill_entry)

    def _extract_cn_keywords(self, skill: Dict) -> List[str]:
        cn_terms = []
        name = skill.get("name", "").lower()
        desc = skill.get("description", "").lower()

        for en_word, cn_words in self.cn_keywords_map.items():
            if en_word in name or en_word in desc:
                cn_terms.extend(cn_words)

        purpose = skill.get("purpose", "").lower()
        for en_word, cn_words in self.cn_keywords_map.items():
            if en_word in purpose:
                cn_terms.extend(cn_words)

        return list(set(cn_terms))

    def search_by_keywords(self, query: str, top_k: int = 10) -> List[SearchResult]:
        query_lower = query.lower()
        is_chinese = bool(re.search(r'[\u4e00-\u9fff]', query))

        scored_skills = []

        for skill in self.all_skills:
            score = 0.0
            reasons = []

            name_lower = skill["name"].lower()
            desc_lower = skill.get("description", "").lower()
            purpose_lower = skill.get("purpose", "").lower()
            cn_keywords = skill.get("cn_keywords", [])

            if is_chinese:
                for cn_word in cn_keywords:
                    if cn_word in query_lower:
                        score += 30
                        reasons.append(f"中文匹配: {cn_word}")
                    if cn_word in desc_lower:
                        score += 15
                    if cn_word in purpose_lower:
                        score += 10

                if query_lower in name_lower:
                    score += 40
                    reasons.append(f"名称包含中文")
                if query_lower in desc_lower:
                    score += 20
                if query_lower in purpose_lower:
                    score += 10
            else:
                query_words = re.findall(r'[\w]+', query_lower)

                for word in query_words:
                    if word in name_lower:
                        score += 30
                        reasons.append(f"名称匹配: {word}")

                    if word in desc_lower:
                        score += 15
                        reasons.append(f"描述包含: {word}")

                    if word in purpose_lower:
                        score += 10

                if score > 0:
                    full_text = f"{name_lower} {desc_lower} {purpose_lower}"
                    for bigram in zip(query_words[:-1], query_words[1:]):
                        phrase = " ".join(bigram)
                        if phrase in full_text:
                            score += 20
                            reasons.append(f"短语匹配: {phrase}")

            if score > 0:
                scored_skills.append(SearchResult(
                    skill=skill,
                    score=score,
                    match_reasons=reasons,
                    category=skill["category_key"],
                    category_emoji=skill["category_emoji"]
                ))

        scored_skills.sort(key=lambda x: -x.score)
        return scored_skills[:top_k]

    def get_by_scenario(self, scenario_key: str) -> List[Dict]:
        if scenario_key in SCENARIO_TEMPLATES:
            scenario = SCENARIO_TEMPLATES[scenario_key]
            results = []
            for skill_name in scenario["recommended"]:
                if skill_name in self.skills_by_name:
                    results.append(self.skills_by_name[skill_name])
                else:
                    for cat_key, skills in self.skills_by_category.items():
                        for s in skills:
                            if skill_name in s["name"]:
                                results.append(s)
                                break
            return results
        return []

    def get_by_category(self, category_key: str) -> List[Dict]:
        return self.skills_by_category.get(category_key, [])

    def get_similar_skills(self, skill_name: str, top_k: int = 5) -> List[SearchResult]:
        if skill_name not in self.skills_by_name:
            return []

        target = self.skills_by_name[skill_name]
        target_categories = {target["category_key"]}

        similar = []
        for skill in self.all_skills:
            if skill["name"] == skill_name:
                continue

            score = 0.0
            reasons = []

            if skill["category_key"] in target_categories:
                score += 30
                reasons.append("同类别")

            name1_set = set(re.findall(r'[\w]+', target["name"].lower()))
            name2_set = set(re.findall(r'[\w]+', skill["name"].lower()))
            overlap = name1_set & name2_set - {"the", "and", "or", "for", "with"}
            if overlap:
                score += len(overlap) * 10
                reasons.append(f"关键词重叠: {', '.join(overlap)}")

            if score > 0:
                similar.append(SearchResult(
                    skill=skill,
                    score=score,
                    match_reasons=reasons,
                    category=skill["category_key"],
                    category_emoji=skill["category_emoji"]
                ))

        similar.sort(key=lambda x: -x.score)
        return similar[:top_k]

    def get_usage_recommendations(self) -> List[Tuple[str, str]]:
        return USAGE_EXAMPLES

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str):
    clear_screen()
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}  {title}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.RESET}\n")

def print_search_results(results: List[SearchResult], title: str = "搜索结果"):
    print(f"\n{Colors.BOLD}{Colors.CYAN}📋 {title}{Colors.RESET}\n")

    if not results:
        print(f"  {Colors.YELLOW}未找到匹配的 Skills{Colors.RESET}")
        return

    for i, result in enumerate(results, 1):
        skill = result.skill
        emoji = result.category_emoji
        print(f"  {Colors.GREEN}{i}{Colors.RESET}. {emoji} {Colors.BOLD}{skill['name']}{Colors.RESET}")
        print(f"     {Colors.YELLOW}分类:{Colors.RESET} {skill.get('category_name', 'N/A')}")
        desc = skill.get('description', '')[:80]
        if desc:
            print(f"     {Colors.YELLOW}描述:{Colors.RESET} {desc}...")
        if result.match_reasons:
            print(f"     {Colors.MAGENTA}匹配:{Colors.RESET} {' | '.join(result.match_reasons[:2])}")
        print()

def display_scenario_menu(finder: SmartSkillFinder):
    print(f"\n{Colors.BOLD}📌 热门场景快速入口:{Colors.RESET}\n")

    for i, (scenario_key, scenario) in enumerate(SCENARIO_TEMPLATES.items(), 1):
        emoji = scenario["emoji"]
        name = scenario["name"]
        print(f"  {Colors.GREEN}{i}{Colors.RESET}. {emoji} {name}")

    print(f"\n  {Colors.YELLOW}0{Colors.RESET}. 返回")

def display_category_menu(finder: SmartSkillFinder):
    print(f"\n{Colors.BOLD}📂 按分类浏览:{Colors.RESET}\n")

    categories = list(finder.skills_by_category.items())
    for i, (cat_key, skills) in enumerate(categories, 1):
        emoji = CATEGORIES_EMOJI.get(cat_key, "⚪")
        print(f"  {Colors.GREEN}{i}{Colors.RESET}. {emoji} {cat_key.title()} ({len(skills)})")

    print(f"\n  {Colors.YELLOW}0{Colors.RESET}. 返回")

def display_skill_detail(skill: Dict, finder: SmartSkillFinder):
    print_header(f"📄 {skill['name']}")

    print(f"  {Colors.BOLD}分类:{Colors.RESET} {skill.get('category_emoji', '')} {skill.get('category_name', 'N/A')}")
    print(f"  {Colors.BOLD}路径:{Colors.RESET} {skill.get('path', 'N/A')}")
    print(f"\n  {Colors.BOLD}描述:{Colors.RESET}")
    desc = skill.get('description', 'N/A')
    print(f"  {desc}")
    print(f"\n  {Colors.BOLD}用途:{Colors.RESET}")
    purpose = skill.get('purpose', 'N/A')
    if len(purpose) > 300:
        purpose = purpose[:300] + "..."
    print(f"  {purpose}")

    similar = finder.get_similar_skills(skill['name'], top_k=3)
    if similar:
        print(f"\n  {Colors.BOLD}相似技能:{Colors.RESET}")
        for s in similar:
            print(f"    {s.category_emoji} {s.skill['name']}")

    print(f"\n  {Colors.BOLD}完整路径:{Colors.RESET}")
    print(f"  {Colors.CYAN}{Path(__file__).parent.parent / skill.get('path', '')}{Colors.RESET}")

def interactive_search(finder: SmartSkillFinder):
    while True:
        print_header("🔍 智能搜索 Skills")

        print("  输入关键词搜索 Skills（例如：Sprint规划、用户故事、API设计）")
        print("  输入场景编号快速进入（例如：输入 5 进入Scrum团队）")
        print(f"\n  {Colors.MAGENTA}快捷场景:{Colors.RESET}")
        for example, scenario_key in finder.get_usage_recommendations():
            scenario = SCENARIO_TEMPLATES.get(scenario_key, {})
            emoji = scenario.get("emoji", "📋")
            print(f"    • \"{example}\" -> {emoji} {scenario.get('name', scenario_key)}")

        print(f"\n  {Colors.YELLOW}0{Colors.RESET}. 返回")

        query = input(f"\n{Colors.BOLD}请输入搜索词或选择场景: {Colors.RESET}").strip()

        if query == '0':
            break

        if query.isdigit():
            idx = int(query) - 1
            scenarios = list(SCENARIO_TEMPLATES.items())
            if 0 <= idx < len(scenarios):
                scenario_key, scenario = scenarios[idx]
                skills = finder.get_by_scenario(scenario_key)
                print_header(f"{scenario['emoji']} {scenario['name']}")
                for i, skill in enumerate(skills, 1):
                    print(f"  {Colors.GREEN}{i}{Colors.RESET}. {skill.get('category_emoji', '')} {Colors.BOLD}{skill['name']}{Colors.RESET}")
                    print(f"     {skill.get('description', '')[:60]}...")
                    print()
                input(f"\n按 Enter 键继续...")
                continue

        results = finder.search_by_keywords(query, top_k=10)
        if results:
            print_search_results(results, f"搜索: '{query}'")
        else:
            print(f"\n  {Colors.YELLOW}未找到匹配 '{query}' 的 Skills，试试其他关键词{Colors.RESET}")

        print(f"  {Colors.YELLOW}0{Colors.RESET}. 返回")
        print(f"  {Colors.CYAN}1-{len(results)}{Colors.RESET}. 查看详情")

        choice = input(f"\n{Colors.BOLD}请选择: {Colors.RESET}").strip()
        if choice == '0':
            break
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                display_skill_detail(results[idx].skill, finder)

        input(f"\n按 Enter 键继续...")

def browse_by_scenario(finder: SmartSkillFinder):
    while True:
        print_header("🎯 场景化推荐")
        display_scenario_menu(finder)

        choice = input(f"\n{Colors.BOLD}请选择场景 (1-{len(SCENARIO_TEMPLATES)}): {Colors.RESET}").strip()

        if choice == '0':
            break

        if choice.isdigit():
            idx = int(choice) - 1
            scenarios = list(SCENARIO_TEMPLATES.items())
            if 0 <= idx < len(scenarios):
                scenario_key, scenario = scenarios[idx]
                skills = finder.get_by_scenario(scenario_key)

                print_header(f"{scenario['emoji']} {scenario['name']}")
                print(f"  {Colors.BOLD}关键词:{Colors.RESET} {', '.join(scenario['keywords'])}\n")

                for i, skill in enumerate(skills, 1):
                    print(f"  {Colors.GREEN}{i}{Colors.RESET}. {skill.get('category_emoji', '')} {Colors.BOLD}{skill['name']}{Colors.RESET}")
                    print(f"     {skill.get('description', '')[:60]}...")
                    print()

                print(f"  {Colors.YELLOW}0{Colors.RESET}. 返回")
                detail_choice = input(f"\n{Colors.BOLD}查看详情 (1-{len(skills)}): {Colors.RESET}").strip()
                if detail_choice.isdigit():
                    idx = int(detail_choice) - 1
                    if 0 <= idx < len(skills):
                        display_skill_detail(skills[idx], finder)

                input(f"\n按 Enter 键继续...")

def browse_by_category(finder: SmartSkillFinder):
    while True:
        print_header("📂 分类浏览")
        display_category_menu(finder)

        choice = input(f"\n{Colors.BOLD}请选择分类 (1-{len(finder.skills_by_category)}): {Colors.RESET}").strip()

        if choice == '0':
            break

        if choice.isdigit():
            idx = int(choice) - 1
            categories = list(finder.skills_by_category.items())
            if 0 <= idx < len(categories):
                cat_key, skills = categories[idx]
                emoji = CATEGORIES_EMOJI.get(cat_key, "⚪")

                print_header(f"{emoji} {cat_key.title()}")

                for i, skill in enumerate(skills, 1):
                    print(f"  {Colors.GREEN}{i}{Colors.RESET}. {Colors.BOLD}{skill['name']}{Colors.RESET}")
                    print(f"     {skill.get('description', '')[:60]}...")
                    print()

                print(f"  {Colors.YELLOW}0{Colors.RESET}. 返回")
                detail_choice = input(f"\n{Colors.BOLD}查看详情 (1-{len(skills)}): {Colors.RESET}").strip()
                if detail_choice.isdigit():
                    idx = int(detail_choice) - 1
                    if 0 <= idx < len(skills):
                        display_skill_detail(skills[idx], finder)

                input(f"\n按 Enter 键继续...")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--search" and len(sys.argv) > 2:
            finder = SmartSkillFinder()
            query = " ".join(sys.argv[2:])
            results = finder.search_by_keywords(query, top_k=10)
            if results:
                print(f"\n🔍 搜索: '{query}'\n")
                for i, result in enumerate(results, 1):
                    skill = result.skill
                    print(f"  {i}. [{skill.get('category_emoji', '')}] {skill['name']}")
                    print(f"     {skill.get('description', '')[:70]}...")
                    print()
            else:
                print(f"\n未找到匹配 '{query}' 的 Skills")
            return
        elif sys.argv[1] == "--scenario" and len(sys.argv) > 2:
            finder = SmartSkillFinder()
            scenario_key = sys.argv[2]
            skills = finder.get_by_scenario(scenario_key)
            if skills:
                print(f"\n🎯 场景: {scenario_key}\n")
                for skill in skills:
                    print(f"  • [{skill.get('category_emoji', '')}] {skill['name']}")
                    print(f"    {skill.get('description', '')[:60]}...")
                    print()
            else:
                print(f"\n未找到场景: {scenario_key}")
            return
        elif sys.argv[1] == "--category" and len(sys.argv) > 2:
            finder = SmartSkillFinder()
            skills = finder.get_by_category(sys.argv[2])
            if skills:
                print(f"\n📂 分类: {sys.argv[2]}\n")
                for skill in skills:
                    print(f"  • {skill['name']}")
                    print(f"    {skill.get('description', '')[:60]}...")
                    print()
            else:
                print(f"\n未找到分类: {sys.argv[2]}")
            return

    while True:
        try:
            print_header("🧠 Smart Skills Finder - 智能 Skills 导航")

            finder = SmartSkillFinder()

            options = [
                ("🔍", "关键词搜索", "输入描述快速找到所需 Skills"),
                ("🎯", "场景化推荐", "按工作场景获取推荐 Skills"),
                ("📂", "分类浏览", "按分类查看所有 Skills"),
                ("📊", "Skills 统计", "查看 Skills 分布情况"),
                ("❓", "使用帮助", "查看使用说明"),
            ]

            print(f"  {Colors.MAGENTA}📦 Skills 总数:{Colors.RESET} {len(finder.all_skills)}\n")

            for emoji, title, desc in options:
                print(f"  {Colors.CYAN}{emoji}{Colors.RESET}  {Colors.BOLD}{title}{Colors.RESET}")
                print(f"      {Colors.YELLOW}{desc}{Colors.RESET}\n")

            print(f"  {Colors.RED}0{Colors.RESET}. 退出\n")

            choice = input(f"{Colors.BOLD}请选择: {Colors.RESET}").strip()

            if choice == '0':
                print(f"\n{Colors.CYAN}再见！👋{Colors.RESET}\n")
                break
            elif choice == '1':
                interactive_search(finder)
            elif choice == '2':
                browse_by_scenario(finder)
            elif choice == '3':
                browse_by_category(finder)
            elif choice == '4':
                print_header("📊 Skills 统计")
                print(f"  {Colors.BOLD}总 Skills 数量:{Colors.RESET} {len(finder.all_skills)}\n")
                print(f"  {Colors.BOLD}分类分布:{Colors.RESET}\n")
                for cat_key, skills in sorted(finder.skills_by_category.items(), key=lambda x: -len(x[1])):
                    emoji = CATEGORIES_EMOJI.get(cat_key, "⚪")
                    bar = "█" * len(skills)
                    print(f"  {emoji} {cat_key.title():<15} {bar} {len(skills)}")
                print()
                input("按 Enter 键继续...")
            elif choice == '5':
                print_header("❓ 使用帮助")
                help_text = """
  Smart Skills Finder 使用指南:

  🔍 关键词搜索
     输入任何描述或关键词，如:
     • "Sprint规划"
     • "用户故事 拆分"
     • "API设计"
     • "Prompt注入"

  🎯 场景化推荐
     选择你的工作场景，获取推荐 Skills:
     • 产品经理基础/高级
     • 敏捷开发/Scrum团队
     • QA测试
     • 独立开发者创业
     • AI产品开发
     • 等等...

  📂 分类浏览
     按15个分类浏览所有118个 Skills

  命令行用法:
    python skill_finder.py --search "Sprint规划"
    python skill_finder.py --scenario scrum_team
    python skill_finder.py --category product
"""
                print(help_text)
                input("按 Enter 键继续...")
            else:
                print(f"\n{Colors.RED}无效选择{Colors.RESET}")
                input()

        except KeyboardInterrupt:
            print(f"\n\n{Colors.CYAN}再见！👋{Colors.RESET}\n")
            break
        except Exception as e:
            print(f"\n{Colors.RED}错误: {e}{Colors.RESET}")
            input()

if __name__ == "__main__":
    main()
