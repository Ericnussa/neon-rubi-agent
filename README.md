# Neon Rubi Agent

A personal **assistant-agent MVP** inspired by Rubi-style operation:

- Persona-driven behavior
- Durable memory (daily + long-term)
- Tool abstraction layer
- Heartbeat loop for proactive checks
- Safe-by-default action policy

## MVP Scope

This MVP provides:

1. **Core Agent Loop** (`app/agent.py`)
2. **Persona + User Profile** (`config/SOUL.md`, `config/USER.md`)
3. **Memory System** (`memory/` + `app/memory.py`)
4. **Heartbeat Task Runner** (`app/heartbeat.py`)
5. **Simple CLI Interface** (`app/main.py`)

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

## Project Layout

```
app/
  main.py
  agent.py
  memory.py
  heartbeat.py
  policy.py
config/
  SOUL.md
  USER.md
memory/
  MEMORY.md
  daily-template.md
scripts/
  bootstrap.sh
```

## Next Steps

- Add model provider adapters (OpenAI/Anthropic/local)
- Add messaging channel adapters (Telegram/Discord/Web)
- Add scheduled task runner (cron + job queue)
- Add plugin tool system
- Add tests + CI workflow

---
Built as a clean, hackable foundation for a self-hosted personal assistant agent.
