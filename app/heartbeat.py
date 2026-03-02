from datetime import datetime, timezone
from app.memory import MemoryStore


class Heartbeat:
    def __init__(self, memory: MemoryStore):
        self.memory = memory

    def run(self) -> str:
        now = datetime.now(timezone.utc)
        self.memory.append_daily(f"Heartbeat check completed at {now.isoformat()}")
        return "HEARTBEAT_OK"
