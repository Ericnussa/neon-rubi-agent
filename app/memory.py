from datetime import datetime, timezone
from pathlib import Path

from app.db import get_conn, init_db


class MemoryStore:
    def __init__(self, memory_dir: Path, db_path: Path | None = None):
        self.memory_dir = memory_dir
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.long_term_file = self.memory_dir / "MEMORY.md"
        self.db_path = db_path

        if not self.long_term_file.exists():
            self.long_term_file.write_text("# Long-Term Memory\n\n", encoding="utf-8")

        if self.db_path:
            init_db(self.db_path)

    def _daily_file(self) -> Path:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return self.memory_dir / f"{date}.md"

    def append_daily(self, text: str) -> None:
        file = self._daily_file()
        timestamp = datetime.now(timezone.utc).strftime("%H:%M UTC")
        with file.open("a", encoding="utf-8") as f:
            f.write(f"- [{timestamp}] {text}\n")

        if self.db_path:
            conn = get_conn(self.db_path)
            conn.execute(
                "INSERT INTO memories (created_at, kind, content) VALUES (?, ?, ?)",
                (datetime.now(timezone.utc).isoformat(), "daily", text),
            )
            conn.commit()
            conn.close()

    def long_term_summary(self) -> str:
        content = self.long_term_file.read_text(encoding="utf-8").strip()
        return content

    def recent_memories(self, limit: int = 20) -> list[dict]:
        if not self.db_path:
            return []
        conn = get_conn(self.db_path)
        rows = conn.execute(
            "SELECT id, created_at, kind, content FROM memories ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
