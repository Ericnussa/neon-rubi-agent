#!/usr/bin/env python3
from pathlib import Path
import secrets

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"


def parse_env(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        if not line or line.strip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def write_env(values: dict[str, str]) -> None:
    lines = [
        "# LLM providers",
        f"OPENAI_API_KEY={values.get('OPENAI_API_KEY','')}",
        f"OPENAI_MODEL={values.get('OPENAI_MODEL','gpt-4o-mini')}",
        f"ANTHROPIC_API_KEY={values.get('ANTHROPIC_API_KEY','')}",
        f"ANTHROPIC_MODEL={values.get('ANTHROPIC_MODEL','claude-3-5-sonnet-latest')}",
        "",
        "# Channels",
        f"TELEGRAM_BOT_TOKEN={values.get('TELEGRAM_BOT_TOKEN','')}",
        f"DISCORD_BOT_TOKEN={values.get('DISCORD_BOT_TOKEN','')}",
        "",
        "# Web UI",
        f"HOST={values.get('HOST','127.0.0.1')}",
        f"PORT={values.get('PORT','8000')}",
        "",
        "# Legacy Admin token endpoint (/admin/memories)",
        f"ADMIN_TOKEN={values.get('ADMIN_TOKEN','')}",
        "",
        "# JWT/Auth",
        f"AUTH_SECRET={values.get('AUTH_SECRET','')}",
        f"ADMIN_USERNAME={values.get('ADMIN_USERNAME','admin')}",
        f"ADMIN_PASSWORD={values.get('ADMIN_PASSWORD','')}",
        "",
        "# Database",
        f"DB_PATH={values.get('DB_PATH','data/neon_rubi.db')}",
        "",
    ]
    ENV_FILE.write_text("\n".join(lines), encoding="utf-8")


def prompt(name: str, current: str, default: str = "") -> str:
    shown = current if current else default
    val = input(f"{name} [{shown}]: ").strip()
    return val if val else shown


if __name__ == "__main__":
    raw = ENV_FILE.read_text(encoding="utf-8") if ENV_FILE.exists() else ""
    values = parse_env(raw)

    print("\nNeon Rubi Agent setup wizard\n")
    values["HOST"] = prompt("HOST", values.get("HOST", ""), "127.0.0.1")
    values["PORT"] = prompt("PORT", values.get("PORT", ""), "8000")
    values["ADMIN_USERNAME"] = prompt("ADMIN_USERNAME", values.get("ADMIN_USERNAME", ""), "admin")

    current_pass = values.get("ADMIN_PASSWORD", "")
    if not current_pass or current_pass == "change-me-now":
        suggested = secrets.token_urlsafe(12)
        entered = input(f"ADMIN_PASSWORD [auto-generate]: ").strip()
        values["ADMIN_PASSWORD"] = entered if entered else suggested
    else:
        values["ADMIN_PASSWORD"] = current_pass

    current_secret = values.get("AUTH_SECRET", "")
    if not current_secret or current_secret == "change-this-secret":
        values["AUTH_SECRET"] = secrets.token_urlsafe(32)

    if not values.get("ADMIN_TOKEN") or values.get("ADMIN_TOKEN") == "change-me":
        values["ADMIN_TOKEN"] = secrets.token_urlsafe(24)

    write_env(values)
    print("\nSaved .env with secure defaults where missing.")
    print("Tip: add OPENAI_API_KEY or ANTHROPIC_API_KEY for best responses.\n")
