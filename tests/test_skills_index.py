#!/usr/bin/env python3
"""
Tests for skills_index module.
Run with: pytest tests/test_skills_index.py -v
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from build_skills_index import build_index, CATEGORIES

SKILLS_ROOT = Path(__file__).parent.parent


def test_categories_defined():
    assert len(CATEGORIES) > 0
    for key, cat in CATEGORIES.items():
        assert "name" in cat
        assert "description" in cat
        assert "sources" in cat
        assert "color" in cat


def test_index_structure():
    index = build_index()

    assert "total_count" in index
    assert "by_category" in index
    assert "last_updated" in index

    assert index["total_count"] > 0
    assert len(index["by_category"]) > 0


def test_category_structure():
    index = build_index()

    for cat_key, cat_data in index["by_category"].items():
        assert "name" in cat_data
        assert "description" in cat_data
        assert "skills" in cat_data
        assert "count" in cat_data

        assert cat_data["count"] > 0
        assert len(cat_data["skills"]) > 0


def test_skill_structure():
    index = build_index()

    for cat_key, cat_data in index["by_category"].items():
        for skill in cat_data["skills"]:
            assert "name" in skill
            assert "description" in skill
            assert "path" in skill


def test_skill_paths_exist():
    index = build_index()

    missing = []
    for cat_key, cat_data in index["by_category"].items():
        for skill in cat_data["skills"]:
            skill_path = SKILLS_ROOT / skill["path"]
            if not skill_path.exists():
                missing.append(skill["path"])

    assert len(missing) == 0, f"Missing skill paths: {missing}"


def test_total_count_matches():
    index = build_index()

    actual_total = sum(len(cat["skills"]) for cat in index["by_category"].values())
    reported_total = index["total_count"]

    assert actual_total == reported_total, \
        f"Mismatch: reported {reported_total}, actual {actual_total}"


def test_categories_match_sources():
    index = build_index()

    for cat_key, cat_data in index["by_category"].items():
        cat_config = CATEGORIES.get(cat_key, {})
        sources = cat_config.get("sources", [])

        for skill in cat_data["skills"]:
            path = skill["path"]
            matched = any(path.startswith(src) for src in sources)
            assert matched, f"Skill {skill['name']} path {path} doesn't match sources {sources}"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
