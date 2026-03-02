from datetime import datetime, timezone
from pathlib import Path


class MemoryStore:
    def __init__(self, memory_dir: Path):
        self.memory_dir = memory_dir
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.long_term_file = self.memory_dir / "MEMORY.md"

        if not self.long_term_file.exists():
            self.long_term_file.write_text("# Long-Term Memory\n\n", encoding="utf-8")

    def _daily_file(self) -> Path:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return self.memory_dir / f"{date}.md"

    def append_daily(self, text: str) -> None:
        file = self._daily_file()
        timestamp = datetime.now(timezone.utc).strftime("%H:%M UTC")
        with file.open("a", encoding="utf-8") as f:
            f.write(f"- [{timestamp}] {text}\n")

    def long_term_summary(self) -> str:
        content = self.long_term_file.read_text(encoding="utf-8").strip()
        return content
