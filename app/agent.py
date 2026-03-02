from pathlib import Path
from app.memory import MemoryStore
from app.policy import ActionPolicy
from app.providers import LLMClient


class AssistantAgent:
    def __init__(self, root: Path | None = None):
        self.root = root or Path.cwd()
        self.memory = MemoryStore(self.root / "memory")
        self.policy = ActionPolicy()
        self.llm = LLMClient()

    def _system_prompt(self) -> str:
        soul = (self.root / "config" / "SOUL.md").read_text(encoding="utf-8")
        user = (self.root / "config" / "USER.md").read_text(encoding="utf-8")
        return f"{soul}\n\n{user}\n\nAlways be helpful and concise."

    def respond(self, message: str) -> str:
        lowered = message.lower()

        if "remember" in lowered:
            note = message.replace("remember", "").strip(": ")
            if note:
                self.memory.append_daily(f"Remembered: {note}")
                return "Got it — I saved that to daily memory."

        if "what do you know about me" in lowered:
            summary = self.memory.long_term_summary()
            return summary or "I don't have long-term notes yet."

        if "send" in lowered or "post" in lowered:
            return self.policy.require_confirmation("external_action")

        self.memory.append_daily(f"User said: {message}")

        if self.llm.is_available():
            try:
                return self.llm.chat(self._system_prompt(), message)
            except Exception:
                pass

        return "I’m on it. Want me to save this as a tracked task too?"
