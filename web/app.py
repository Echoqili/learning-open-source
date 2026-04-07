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
from pathlib import Path
from datetime import datetime
from functools import lru_cache

from flask import Flask, render_template, request, jsonify, send_file, Response

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

SKILLS_ROOT = Path(__file__).parent.parent
INDEX_PATH = SKILLS_ROOT / "skills-index.json"

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
    print("🧠 Skills Manager Web - 可视化 Skills 导航")
    print("=" * 60)
    print(f"\n📦 Skills 索引: {INDEX_PATH}")
    print(f"🌐 访问地址: http://127.0.0.1:5555")
    print("\n按 Ctrl+C 停止服务器\n")

    app.run(host='0.0.0.0', port=5555, debug=True)
