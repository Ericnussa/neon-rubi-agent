# VPS One-Command Deploy (Docker)

Run this on your VPS:

```bash
git clone https://github.com/Ericnussa/neon-rubi-agent.git && cd neon-rubi-agent && cp .env.example .env && nano .env && docker compose up -d --build
```

Required `.env` values:
- `AUTH_SECRET`
- `ADMIN_PASSWORD`
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`

Then open:
- `http://YOUR_VPS_IP:8000`
