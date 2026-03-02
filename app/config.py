import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")

    telegram_bot_token: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
    discord_bot_token: str | None = os.getenv("DISCORD_BOT_TOKEN")

    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))

    admin_token: str | None = os.getenv("ADMIN_TOKEN")
    db_path: Path = Path(os.getenv("DB_PATH", "data/neon_rubi.db"))

    auth_secret: str = os.getenv("AUTH_SECRET", "change-this-secret")
    admin_username: str = os.getenv("ADMIN_USERNAME", "admin")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "change-me")
