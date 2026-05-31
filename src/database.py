import sqlite3
import os
from contextlib import contextmanager


DB_DIR = os.path.join(os.path.expanduser("~"), ".translator-app")
DB_PATH = os.path.join(DB_DIR, "data.db")


def _ensure_db():
    os.makedirs(DB_DIR, exist_ok=True)


@contextmanager
def get_connection():
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS word_book (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                translation TEXT NOT NULL,
                source_lang TEXT DEFAULT 'auto',
                target_lang TEXT DEFAULT 'zh',
                note TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text TEXT NOT NULL,
                translation TEXT NOT NULL,
                source_lang TEXT DEFAULT 'auto',
                target_lang TEXT DEFAULT 'zh',
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        conn.commit()


def save_to_word_book(word: str, translation: str, note: str = ""):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO word_book (word, translation, note) VALUES (?, ?, ?)",
            (word, translation, note),
        )
        conn.commit()


def delete_word(word_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM word_book WHERE id = ?", (word_id,))
        conn.commit()


def get_all_words() -> list:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM word_book ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]


def search_words(keyword: str) -> list:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM word_book WHERE word LIKE ? OR translation LIKE ? ORDER BY created_at DESC",
            (f"%{keyword}%", f"%{keyword}%"),
        ).fetchall()
        return [dict(r) for r in rows]


def add_history(source: str, translation: str, source_lang: str = "auto", target_lang: str = "zh"):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO history (source_text, translation, source_lang, target_lang) VALUES (?, ?, ?, ?)",
            (source, translation, source_lang, target_lang),
        )
        conn.commit()


def get_history(limit: int = 100) -> list:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM history ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def clear_history():
    with get_connection() as conn:
        conn.execute("DELETE FROM history")
        conn.commit()


def get_setting(key: str, default: str = "") -> str:
    with get_connection() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else default


def set_setting(key: str, value: str):
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value),
        )
        conn.commit()


def clear_word_book():
    with get_connection() as conn:
        conn.execute("DELETE FROM word_book")
        conn.commit()
