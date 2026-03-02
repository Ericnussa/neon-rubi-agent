# Deploy Guide

## Option A — Docker (recommended)

```bash
cp .env.example .env
# fill in API keys/tokens

docker compose up -d --build
```

Open: `http://YOUR_SERVER_IP:8000`

## Option B — Bare metal (venv)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
./scripts/run-web.sh
```

## Running Telegram/Discord

```bash
source .venv/bin/activate
python -m app.main --mode telegram
# or
python -m app.main --mode discord
```

## Suggested Production Hardening

- Put Caddy/Nginx in front with HTTPS
- Run under systemd for process supervision
- Restrict tokens to least required permissions
- Set explicit model names in `.env`
