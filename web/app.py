#!/usr/bin/env python3
"""
Skills Manager Web - 可视化 Web 端
提供 Skills 搜索、浏览、打包下载的可视化界面
"""

import os
import sys
import json
import re
import zipfile
import requests
from pathlib import Path
from datetime import datetime
from functools import lru_cache

from flask import Flask, render_template, request, jsonify, send_file, Response

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

SKILLS_ROOT = Path(__file__).parent.parent
INDEX_PATH = SKILLS_ROOT / "skills-index.json"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

GITHUB_HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Skills-Manager/1.0"
}
if GITHUB_TOKEN:
    GITHUB_HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

CATEGORIES_EMOJI = {
    "product": "🔵", "agile": "🟢", "scrum": "🟡", "ddd": "🟠",
    "dev-quality": "🟣", "qa-testing": "🔴", "api-design": "⚪",
    "ai-product": "🩵", "ai-safety": "🚨", "superpowers": "⚡",
    "dev-workflow": "🔧", "design": "🎨", "skill-authoring": "🛠️", "indie-hacker": "💰"
}

SCENARIOS = {
    "pm_basics": {"name": "产品经理基础", "emoji": "📋"},
    "pm_advanced": {"name": "高级产品经理", "emoji": "🎯"},
    "customer_discovery": {"name": "客户探索验证", "emoji": "🔍"},
    "agile_dev": {"name": "敏捷开发团队", "emoji": "🏃"},
    "scrum_team": {"name": "Scrum团队", "emoji": "🎯"},
    "qa_testing": {"name": "QA与测试", "emoji": "🧪"},
    "architecture": {"name": "架构设计", "emoji": "🏗️"},
    "dev_quality": {"name": "开发质量", "emoji": "💎"},
    "tdd_workflow": {"name": "TDD测试驱动", "emoji": "⚡"},
    "indie_hacker": {"name": "独立开发者创业", "emoji": "💰"},
    "ai_product": {"name": "AI产品开发", "emoji": "🤖"},
    "design_system": {"name": "设计系统", "emoji": "🎨"},
    "skill_creation": {"name": "Skill开发", "emoji": "🛠️"}
}


@lru_cache(maxsize=1)
def load_index():
    if INDEX_PATH.exists():
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"by_category": {}, "total_count": 0}


def build_skills_cache():
    index = load_index()
    all_skills = []
    skills_by_name = {}
    skills_by_category = {}

    for cat_key, cat_info in index.get("by_category", {}).items():
        emoji = CATEGORIES_EMOJI.get(cat_key, "⚪")
        skills_by_category[cat_key] = []

        for skill in cat_info.get("skills", []):
            skill_entry = {
                **skill,
                "category_key": cat_key,
                "category_name": cat_info["name"],
                "category_emoji": emoji
            }
            all_skills.append(skill_entry)
            skills_by_name[skill["name"]] = skill_entry
            skills_by_category[cat_key].append(skill_entry)

    return all_skills, skills_by_name, skills_by_category


def search_skills(query, top_k=20):
    if not query:
        return []

    all_skills, _, _ = build_skills_cache()
    query_lower = query.lower()
    is_chinese = bool(re.search(r'[\u4e00-\u9fff]', query))

    results = []

    for skill in all_skills:
        score = 0
        name_lower = skill["name"].lower()
        desc_lower = skill.get("description", "").lower()

        if is_chinese:
            if query_lower in name_lower or query_lower in desc_lower:
                score = 50
        else:
            query_words = re.findall(r'[\w]+', query_lower)
            for word in query_words:
                if word in name_lower:
                    score += 30
                if word in desc_lower:
                    score += 15

        if score > 0:
            results.append((score, skill))

    results.sort(key=lambda x: -x[0])
    return [s for _, s in results[:top_k]]


def search_github_repos(query: str, per_page: int = 10):
    """Search GitHub repositories for skills"""
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "per_page": per_page, "sort": "stars", "order": "desc"}

    try:
        resp = requests.get(url, headers=GITHUB_HEADERS, params=params, timeout=30)
        if resp.status_code == 200:
            return resp.json().get("items", [])
        elif resp.status_code == 403:
            return {"error": "rate_limited", "message": "GitHub API rate limit exceeded"}
        elif resp.status_code == 422:
            return {"error": "invalid_query", "message": "Invalid search query"}
        return {"error": "unknown", "message": f"GitHub API returned {resp.status_code}"}
    except Exception as e:
        return {"error": "network", "message": str(e)}


def get_ai_recommendation(query: str, local_results: list):
    """Get AI-powered recommendation based on query and local results"""
    if not query:
        return {
            "recommendation": "请输入关键词，我会为您推荐合适的 Skills",
            "suggestions": []
        }

    query_lower = query.lower()

    recommendations = {
        "sprint": {
            "name": "Sprint 规划与管理",
            "emoji": "🏃",
            "skills": ["sprint-planning", "backlog-refinement", "retrospective", "sprint-review"],
            "reason": "您似乎在关注 Sprint 相关的工作流程"
        },
        "test": {
            "name": "测试与质量保障",
            "emoji": "🧪",
            "skills": ["playwright-automation", "e2e-testing", "unit-testing", "test-strategy"],
            "reason": "您似乎需要测试相关的技能"
        },
        "prd": {
            "name": "产品需求文档",
            "emoji": "📋",
            "skills": ["prd-development", "user-story", "discovery-process"],
            "reason": "您似乎在准备 PRD 或产品需求文档"
        },
        "api": {
            "name": "API 设计",
            "emoji": "🌐",
            "skills": ["api-generator", "rest-api-design", "graphql-api"],
            "reason": "您似乎在关注 API 设计与开发"
        },
        "ddd": {
            "name": "领域驱动设计",
            "emoji": "🏗️",
            "skills": ["ddd-skills", "hexagonal-architecture", "domain-modeling"],
            "reason": "您似乎在关注 DDD 架构设计"
        },
        "安全": {
            "name": "AI 安全",
            "emoji": "🚨",
            "skills": ["prompt-injection-defense", "jailbreak-detection", "hallucination-detection"],
            "reason": "您似乎在关注 AI 安全问题"
        },
        "ai": {
            "name": "AI 产品开发",
            "emoji": "🤖",
            "skills": ["ai-product", "prompt-engineering", "llm-integration"],
            "reason": "您似乎在开发 AI 相关产品"
        },
        "tdd": {
            "name": "测试驱动开发",
            "emoji": "⚡",
            "skills": ["tdd-workflow", "test-driven-development", "red-green-refactor"],
            "reason": "您似乎在实践 TDD 开发流程"
        },
        "mvp": {
            "name": "快速 MVP 开发",
            "emoji": "💰",
            "skills": ["validate-idea", "mvp", "first-customers", "pricing"],
            "reason": "您似乎在准备独立开发或创业"
        },
        "design": {
            "name": "设计系统",
            "emoji": "🎨",
            "skills": ["design-system", "ui-ux-pro-max", "component-library"],
            "reason": "您似乎在关注设计与用户体验"
        }
    }

    matched = []
    for key, rec in recommendations.items():
        if key in query_lower:
            matched.append(rec)

    if matched:
        best_match = matched[0]
        return {
            "recommendation": f"🤖 {best_match['reason']}",
            "category": best_match["name"],
            "emoji": best_match["emoji"],
            "suggestions": best_match["skills"],
            "source": "ai_recommendation"
        }

    if local_results:
        top_result = local_results[0]
        return {
            "recommendation": f"🤖 根据您的搜索 '{query}'，我们推荐 {top_result.get('category_name', '相关')} 类别的 Skills",
            "suggestions": [s["name"] for s in local_results[:5]],
            "source": "ai_recommendation"
        }

    return {
        "recommendation": f"🤖 未能理解您的需求。请尝试：Sprint规划、测试策略、API设计、AI安全等关键词",
        "suggestions": ["sprint-planning", "test-strategy", "api-generator", "prompt-injection-defense"],
        "source": "ai_recommendation"
    }


def get_skill_dir(skill):
    skill_path = SKILLS_ROOT / skill.get("path", "")
    if skill_path.is_file():
        skill_path = skill_path.parent
    return skill_path


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/stats')
def stats():
    index = load_index()
    total = index.get("total_count", 0)
    by_category = index.get("by_category", {})

    categories = []
    for cat_key, cat_info in by_category.items():
        emoji = CATEGORIES_EMOJI.get(cat_key, "⚪")
        categories.append({
            "key": cat_key,
            "name": cat_info["name"],
            "emoji": emoji,
            "count": len(cat_info.get("skills", []))
        })

    categories.sort(key=lambda x: -x["count"])

    return jsonify({
        "total": total,
        "categories": categories
    })


@app.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    results = search_skills(query)

    return jsonify({
        "query": query,
        "count": len(results),
        "results": results[:20]
    })


@app.route('/api/search/github')
def api_search_github():
    query = request.args.get('q', '')
    per_page = request.args.get('per_page', 10, type=int)

    if not query:
        return jsonify({"error": "Query is required"}), 400

    enhanced_query = f"{query} skills site:github.com"
    repos = search_github_repos(enhanced_query, per_page)

    if isinstance(repos, dict) and "error" in repos:
        return jsonify(repos), 429 if repos["error"] == "rate_limited" else 400

    formatted = []
    for repo in repos:
        formatted.append({
            "name": repo.get("full_name", ""),
            "description": repo.get("description", ""),
            "stars": repo.get("stargazers_count", 0),
            "url": repo.get("html_url", ""),
            "language": repo.get("language", ""),
            "updated": repo.get("updated_at", "")[:10]
        })

    return jsonify({
        "query": query,
        "count": len(formatted),
        "repos": formatted
    })


@app.route('/api/search/ai')
def api_search_ai():
    query = request.args.get('q', '')

    local_results = search_skills(query)
    recommendation = get_ai_recommendation(query, local_results)

    return jsonify({
        "query": query,
        "recommendation": recommendation,
        "local_results_count": len(local_results)
    })


@app.route('/api/search/all')
def api_search_all():
    query = request.args.get('q', '')

    if not query:
        return jsonify({"error": "Query is required"}), 400

    local_results = search_skills(query)
    recommendation = get_ai_recommendation(query, local_results)

    enhanced_query = f"{query} skills site:github.com"
    github_repos = search_github_repos(enhanced_query, 5)

    github_data = []
    if isinstance(github_repos, list):
        for repo in github_repos[:5]:
            github_data.append({
                "name": repo.get("full_name", ""),
                "description": repo.get("description", ""),
                "stars": repo.get("stargazers_count", 0),
                "url": repo.get("html_url", ""),
            })

    return jsonify({
        "query": query,
        "recommendation": recommendation,
        "local": {
            "count": len(local_results),
            "results": local_results[:5]
        },
        "github": {
            "count": len(github_data),
            "repos": github_data
        }
    })


@app.route('/api/category/<cat_key>')
def api_category(cat_key):
    _, _, skills_by_category = build_skills_cache()
    skills = skills_by_category.get(cat_key, [])
    return jsonify({
        "key": cat_key,
        "count": len(skills),
        "skills": skills
    })


@app.route('/api/scenario/<scenario_key>')
def api_scenario(scenario_key):
    scenario = SCENARIOS.get(scenario_key)
    if not scenario:
        return jsonify({"error": "Scenario not found"}), 404

    _, skills_by_name, skills_by_category = build_skills_cache()

    scenario_skills_map = {
        "pm_basics": ["discovery-process", "user-story", "prd-development", "prioritization-advisor", "product-strategy-session"],
        "pm_advanced": ["business-health-diagnostic", "saas-economics-efficiency-metrics", "executive-onboarding-playbook"],
        "customer_discovery": ["discovery-interview-prep", "discovery-process", "customer-journey-map", "problem-statement"],
        "agile_dev": ["sprint-planning", "backlog-refinement", "retrospective", "definition-of-done-enforcer"],
        "scrum_team": ["sprint-planning", "sprint-review", "retrospective", "backlog-refinement", "smoke-test"],
        "qa_testing": ["test-strategy", "playwright-automation", "e2e-testing", "unit-testing"],
        "architecture": ["ddd-skills", "api-generator"],
        "dev_quality": ["clean-code", "debugger", "git-workflow", "coding-standards"],
        "tdd_workflow": ["tdd-workflow", "test-driven-development", "systematic-debugging"],
        "indie_hacker": ["validate-idea", "mvp", "first-customers", "pricing", "marketing-plan"],
        "ai_product": ["ai-product", "prompt-injection-defense", "hallucination-detection"],
        "design_system": ["design-system", "ui-ux-pro-max"],
        "skill_creation": ["skill-creator"]
    }

    skill_names = scenario_skills_map.get(scenario_key, [])
    skills = []
    for name in skill_names:
        if name in skills_by_name:
            skills.append(skills_by_name[name])

    return jsonify({
        "key": scenario_key,
        "name": scenario["name"],
        "emoji": scenario["emoji"],
        "count": len(skills),
        "skills": skills
    })


@app.route('/api/skill/<path:skill_name>')
def api_skill(skill_name):
    _, skills_by_name, _ = build_skills_cache()

    for name, skill in skills_by_name.items():
        if skill_name in name or name in skill_name:
            skill_dir = get_skill_dir(skill)
            files = []
            if skill_dir.exists():
                for f in skill_dir.rglob("*"):
                    if f.is_file():
                        rel_path = f.relative_to(skill_dir)
                        files.append({
                            "name": rel_path.name,
                            "path": str(rel_path),
                            "size": f.stat().st_size
                        })

            return jsonify({
                "name": skill["name"],
                "description": skill.get("description", ""),
                "category": skill.get("category_name", ""),
                "emoji": skill.get("category_emoji", ""),
                "path": str(skill_dir.relative_to(SKILLS_ROOT)),
                "files": files
            })

    return jsonify({"error": "Skill not found"}), 404


@app.route('/api/package', methods=['POST'])
def api_package():
    data = request.get_json()
    skill_names = data.get('skills', [])
    package_type = data.get('type', 'custom')

    _, skills_by_name, _ = build_skills_cache()

    skills_to_package = []
    for name in skill_names:
        if name in skills_by_name:
            skills_to_package.append(skills_by_name[name])

    if not skills_to_package:
        return jsonify({"error": "No valid skills to package"}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"skills_{package_type}_{timestamp}.zip"
    output_path = SKILLS_ROOT / filename

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for skill in skills_to_package:
            skill_dir = get_skill_dir(skill)
            if skill_dir.exists():
                for file_path in skill_dir.rglob("*"):
                    if file_path.is_file():
                        arcname = f"{skill['name']}/{file_path.relative_to(skill_dir)}"
                        zf.write(file_path, arcname)

    return jsonify({
        "success": True,
        "filename": filename,
        "size": output_path.stat().st_size,
        "count": len(skills_to_package)
    })


@app.route('/download/<path:filename>')
def download(filename):
    if not filename.endswith('.zip'):
        filename += '.zip'

    file_path = SKILLS_ROOT / filename
    if not file_path.exists():
        return jsonify({"error": "File not found"}), 404

    return send_file(
        file_path,
        mimetype='application/zip',
        as_attachment=True,
        download_name=filename
    )


@app.route('/api/package-all', methods=['POST'])
def api_package_all():
    _, _, skills_by_category = build_skills_cache()

    all_skills = []
    for skills in skills_by_category.values():
        all_skills.extend(skills)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"all_skills_{timestamp}.zip"
    output_path = SKILLS_ROOT / filename

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for skill in all_skills:
            skill_dir = get_skill_dir(skill)
            if skill_dir.exists():
                for file_path in skill_dir.rglob("*"):
                    if file_path.is_file():
                        arcname = f"{skill['name']}/{file_path.relative_to(skill_dir)}"
                        zf.write(file_path, arcname)

    return jsonify({
        "success": True,
        "filename": filename,
        "size": output_path.stat().st_size,
        "count": len(all_skills)
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Skills Manager Web - 可视化 Skills 导航")
    print("=" * 60)
    print(f"\nSkills 索引: {INDEX_PATH}")
    print(f"访问地址: http://127.0.0.1:5555")
    print("\n按 Ctrl+C 停止服务器\n")

    app.run(host='0.0.0.0', port=5555, debug=True)
