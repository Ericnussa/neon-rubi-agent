from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from app.db import get_conn, init_db


class ChatStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        init_db(db_path)

    def create_thread(self, title: str, owner_username: str | None = None) -> int:
        conn = get_conn(self.db_path)
        cur = conn.execute(
            "INSERT INTO threads (created_at, title, owner_username) VALUES (?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), title, owner_username),
        )
        conn.commit()
        tid = int(cur.lastrowid)
        conn.close()
        return tid

    def add_message(self, thread_id: int, role: str, content: str) -> int:
        conn = get_conn(self.db_path)
        cur = conn.execute(
            "INSERT INTO messages (thread_id, created_at, role, content) VALUES (?, ?, ?, ?)",
            (thread_id, datetime.now(timezone.utc).isoformat(), role, content),
        )
        conn.commit()
        mid = int(cur.lastrowid)
        conn.close()
        return mid

    def list_threads(self, limit: int = 50) -> list[dict]:
        conn = get_conn(self.db_path)
        rows = conn.execute(
            "SELECT id, created_at, title, owner_username FROM threads ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_messages(self, thread_id: int, limit: int = 200) -> list[dict]:
        conn = get_conn(self.db_path)
        rows = conn.execute(
            "SELECT id, thread_id, created_at, role, content FROM messages WHERE thread_id = ? ORDER BY id ASC LIMIT ?",
            (thread_id, limit),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
