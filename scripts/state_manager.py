#!/usr/bin/env python3
"""
State persistence module for Skills Manager.

Manages application state including:
- Recent searches
- Bookmarked skills
- Download history
- User preferences
- Cart state
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


STATE_DIR = Path(__file__).parent.parent / ".state"
STATE_FILE = STATE_DIR / "app_state.json"


@dataclass
class SearchHistory:
    query: str
    timestamp: str
    results_count: int = 0


@dataclass
class BookmarkedSkill:
    name: str
    category: str
    bookmarked_at: str
    notes: str = ""


@dataclass
class DownloadRecord:
    filename: str
    skills_count: int
    size_bytes: int
    downloaded_at: str
    download_type: str


@dataclass
class UserPreferences:
    theme: str = "light"
    default_category: str = "product"
    search_language: str = "auto"
    items_per_page: int = 20
    show_skill_preview: bool = True


@dataclass
class CartItem:
    name: str
    added_at: str


@dataclass
class AppState:
    version: str = "1.0.0"
    last_updated: str = ""
    search_history: list = field(default_factory=list)
    bookmarks: list = field(default_factory=list)
    download_history: list = field(default_factory=list)
    cart: list = field(default_factory=list)
    preferences: UserPreferences = field(default_factory=UserPreferences)


class StateManager:
    _instance: Optional["StateManager"] = None

    def __new__(cls) -> "StateManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._state = AppState()
        self._ensure_state_dir()
        self._load()

    def _ensure_state_dir(self) -> None:
        STATE_DIR.mkdir(parents=True, exist_ok=True)

    def _load(self) -> None:
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._state = AppState(
                        version=data.get("version", "1.0.0"),
                        last_updated=data.get("last_updated", ""),
                        search_history=[SearchHistory(**s) for s in data.get("search_history", [])],
                        bookmarks=[BookmarkedSkill(**b) for b in data.get("bookmarks", [])],
                        download_history=[DownloadRecord(**d) for d in data.get("download_history", [])],
                        cart=[CartItem(**c) for c in data.get("cart", [])],
                        preferences=UserPreferences(**data.get("preferences", {}))
                    )
            except (json.JSONDecodeError, TypeError) as e:
                print(f"[StateManager] Warning: Failed to load state: {e}")

    def _save(self) -> None:
        self._state.last_updated = datetime.now().isoformat()
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(asdict(self._state), f, indent=2, ensure_ascii=False)

    def add_search(self, query: str, results_count: int = 0) -> None:
        entry = SearchHistory(
            query=query,
            timestamp=datetime.now().isoformat(),
            results_count=results_count
        )
        self._state.search_history.insert(0, entry)
        self._state.search_history = self._state.search_history[:50]
        self._save()

    def get_recent_searches(self, limit: int = 10) -> list:
        return self._state.search_history[:limit]

    def clear_search_history(self) -> None:
        self._state.search_history = []
        self._save()

    def add_bookmark(self, name: str, category: str, notes: str = "") -> bool:
        for b in self._state.bookmarks:
            if b.name == name:
                return False
        self._state.bookmarks.append(BookmarkedSkill(
            name=name,
            category=category,
            bookmarked_at=datetime.now().isoformat(),
            notes=notes
        ))
        self._save()
        return True

    def remove_bookmark(self, name: str) -> bool:
        for i, b in enumerate(self._state.bookmarks):
            if b.name == name:
                self._state.bookmarks.pop(i)
                self._save()
                return True
        return False

    def get_bookmarks(self) -> list:
        return self._state.bookmarks

    def add_download(self, filename: str, skills_count: int, size_bytes: int, download_type: str) -> None:
        self._state.download_history.insert(0, DownloadRecord(
            filename=filename,
            skills_count=skills_count,
            size_bytes=size_bytes,
            downloaded_at=datetime.now().isoformat(),
            download_type=download_type
        ))
        self._state.download_history = self._state.download_history[:100]
        self._save()

    def get_download_history(self, limit: int = 20) -> list:
        return self._state.download_history[:limit]

    def add_to_cart(self, name: str) -> bool:
        for c in self._state.cart:
            if c.name == name:
                return False
        self._state.cart.append(CartItem(
            name=name,
            added_at=datetime.now().isoformat()
        ))
        self._save()
        return True

    def remove_from_cart(self, name: str) -> bool:
        for i, c in enumerate(self._state.cart):
            if c.name == name:
                self._state.cart.pop(i)
                self._save()
                return True
        return False

    def get_cart(self) -> list:
        return self._state.cart

    def clear_cart(self) -> None:
        self._state.cart = []
        self._save()

    def get_preferences(self) -> UserPreferences:
        return self._state.preferences

    def update_preferences(self, **kwargs) -> None:
        prefs = self._state.preferences
        for key, value in kwargs.items():
            if hasattr(prefs, key):
                setattr(prefs, key, value)
        self._save()

    def get_stats(self) -> dict:
        return {
            "total_searches": len(self._state.search_history),
            "total_bookmarks": len(self._state.bookmarks),
            "total_downloads": len(self._state.download_history),
            "cart_items": len(self._state.cart),
            "last_updated": self._state.last_updated
        }

    def export_state(self, path: Optional[Path] = None) -> Path:
        if path is None:
            path = STATE_DIR / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self._state), f, indent=2, ensure_ascii=False)
        return path

    def import_state(self, path: Path) -> bool:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._state = AppState(
                version=data.get("version", "1.0.0"),
                last_updated=datetime.now().isoformat(),
                search_history=[SearchHistory(**s) for s in data.get("search_history", [])],
                bookmarks=[BookmarkedSkill(**b) for b in data.get("bookmarks", [])],
                download_history=[DownloadRecord(**d) for d in data.get("download_history", [])],
                cart=[CartItem(**c) for c in data.get("cart", [])],
                preferences=UserPreferences(**data.get("preferences", {}))
            )
            self._save()
            return True
        except Exception as e:
            print(f"[StateManager] Import failed: {e}")
            return False


_state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager
