# Cloud Deploy Options

## Railway (One Click)

1. Click: https://railway.com/deploy?repo=https://github.com/Ericnussa/neon-rubi-agent
2. Add env vars:
   - `AUTH_SECRET`
   - `ADMIN_USERNAME`
   - `ADMIN_PASSWORD`
   - `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
3. Deploy and open generated URL.

## Render (Blueprint)

1. In Render: New + > Blueprint
2. Point to this repo
3. Render reads `render.yaml`
4. Set missing secrets in dashboard

## Fly.io

```bash
fly launch
fly secrets set AUTH_SECRET=... ADMIN_USERNAME=admin ADMIN_PASSWORD=... OPENAI_API_KEY=...
fly deploy
```

Uses `fly.toml` from repo.
