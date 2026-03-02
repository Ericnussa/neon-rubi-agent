# Neon Rubi Agent

[![CI](https://github.com/Ericnussa/neon-rubi-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Ericnussa/neon-rubi-agent/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Ericnussa/neon-rubi-agent)](https://github.com/Ericnussa/neon-rubi-agent/releases)
[![Deploy Workflow](https://img.shields.io/badge/deploy-manual-blue)](https://github.com/Ericnussa/neon-rubi-agent/actions/workflows/deploy.yml)


## 🚀 DEPLOY NOW

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy?repo=https://github.com/Ericnussa/neon-rubi-agent)
[![Open Deploy Workflow](https://img.shields.io/badge/GitHub%20Actions-Deploy%20GHCR-blue?logo=githubactions)](https://github.com/Ericnussa/neon-rubi-agent/actions/workflows/deploy.yml)
[![Open Releases](https://img.shields.io/badge/GitHub-Releases-181717?logo=github)](https://github.com/Ericnussa/neon-rubi-agent/releases)

**Fastest path:** click Railway button → set env vars → deploy.


A personal **assistant-agent** starter inspired by Rubi-style operation:

- Persona-driven behavior
- Durable memory (daily + long-term)
- LLM provider adapters (OpenAI + Anthropic)
- Channel adapters (CLI + Telegram + Discord)
- Lightweight web UI (FastAPI)
- Admin-token protected dashboard endpoint
- SQLite-backed persistent memory
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

## Auth

- Login endpoint: `POST /auth/login` (username/password)
- JWT-protected admin endpoint: `GET /admin/memories-jwt`
- Legacy admin token endpoint: `GET /admin/memories` with `x-admin-token`

## Notes

- If no provider key is set, the agent gracefully falls back to basic local responses.
- External/public actions are blocked behind confirmation messaging by default.
- Memory writes are UTC timestamped markdown logs and mirrored to SQLite (`data/neon_rubi.db`).
- `/admin/memories` requires `x-admin-token` header matching `ADMIN_TOKEN`.

## Next Suggested Upgrades

- Task queue + scheduler for autonomous jobs
- Tool/plugin registry with permission scopes
- Retrieval from long-term memory (semantic search)
- Tests + GitHub Actions CI
- Docker deployment


## Roles & Auth

- Roles: `admin`, `editor`, `viewer`
- `POST /auth/login` returns JWT with role claim
- `POST /admin/users` (admin only) creates users
- `GET /admin/memories-jwt` requires JWT (viewer+)

## Threaded Chat History API

- `POST /threads` (editor+) create thread
- `GET /threads` (viewer+) list threads
- `POST /threads/{id}/messages` (editor+) add message
- `GET /threads/{id}/messages` (viewer+) read messages


## Full Web UI

The `/` route now ships a complete built-in UI with:
- JWT login/logout
- Role-aware admin panel (create users)
- Thread list + thread creation
- Message timeline
- Composer that writes both user + assistant messages to thread history


## One-Command Install

```bash
./scripts/install.sh
```

Installer flow:
- creates `.venv`
- installs dependencies
- copies `.env.example` to `.env` (if needed)
- runs interactive setup wizard
- auto-generates secure defaults for auth secrets/tokens

## Secure Config Check

```bash
python scripts/security_check.py
```

Fails if insecure defaults are still present.

## Packaged Docs

- `docs/QUICKSTART.md` for non-developers
- `DEPLOY.md` for server deployment


## One-Click Actions

- **Run Deploy Workflow:** https://github.com/Ericnussa/neon-rubi-agent/actions/workflows/deploy.yml
- **Releases:** https://github.com/Ericnussa/neon-rubi-agent/releases
- **Latest Release (v0.1.0):** https://github.com/Ericnussa/neon-rubi-agent/releases/tag/v0.1.0


## One-Click Cloud Deploy

- **Railway:** [![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy?repo=https://github.com/Ericnussa/neon-rubi-agent)
- **Render:** Use Blueprint from this repo (`render.yaml`) in Render dashboard
- **Fly.io:** `fly launch` in repo (uses `fly.toml`)


- **Heroku:** one-click app manifest via `app.json` + `Procfile`
- **Koyeb:** config scaffold via `koyeb.yaml`
- **Zeabur:** config scaffold via `zeabur.json`

### Deploy Notes
- Set required secrets/env vars in your platform dashboard (`AUTH_SECRET`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and at least one LLM API key).
- For public deployments, always rotate default credentials.
