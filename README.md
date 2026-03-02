# Neon Rubi Agent

A personal **assistant-agent** starter inspired by Rubi-style operation:

- Persona-driven behavior
- Durable memory (daily + long-term)
- LLM provider adapters (OpenAI + Anthropic)
- Channel adapters (CLI + Telegram + Discord)
- Lightweight web UI (FastAPI)
- Heartbeat + safety policy primitives

## MVP+ Scope (implemented)

- **Core Agent Loop** (`app/agent.py`)
- **Persona + User Profile** (`config/SOUL.md`, `config/USER.md`)
- **Memory System** (`memory/` + `app/memory.py`)
- **LLM Layer** (`app/providers.py`)
- **Channel Connectors** (`app/channels.py`)
- **Web Chat UI** (`app/web.py`)
- **Action Confirmation Policy** (`app/policy.py`)

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then set API keys/tokens
```

### 1) CLI mode

```bash
python -m app.main
```

### 2) Telegram bot mode

```bash
export TELEGRAM_BOT_TOKEN=your_token
python -m app.main --mode telegram
```

### 3) Discord bot mode

```bash
export DISCORD_BOT_TOKEN=your_token
python -m app.main --mode discord
```

### 4) Web UI mode

```bash
./scripts/run-web.sh
# open http://127.0.0.1:8000
```

## Project Layout

```
app/
  main.py
  agent.py
  memory.py
  providers.py
  channels.py
  heartbeat.py
  policy.py
  web.py
config/
  SOUL.md
  USER.md
memory/
  MEMORY.md
  daily-template.md
scripts/
  bootstrap.sh
  run-web.sh
  run-telegram.sh
  run-discord.sh
.env.example
```

## Notes

- If no provider key is set, the agent gracefully falls back to basic local responses.
- External/public actions are blocked behind confirmation messaging by default.
- Memory writes are UTC timestamped markdown logs for easy auditing.

## Next Suggested Upgrades

- Task queue + scheduler for autonomous jobs
- Tool/plugin registry with permission scopes
- Retrieval from long-term memory (semantic search)
- Tests + GitHub Actions CI
- Docker deployment
