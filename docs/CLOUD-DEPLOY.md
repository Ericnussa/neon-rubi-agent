# Cloud Deploy Options

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


## Heroku

1. Create app in Heroku dashboard
2. Connect this GitHub repo
3. Heroku reads `Procfile` + `app.json`
4. Set env vars: `AUTH_SECRET`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`

## Koyeb

1. Create service from GitHub repo
2. Use Dockerfile deploy
3. Optionally import `koyeb.yaml` settings
4. Replace placeholder secrets before deploy

## Zeabur

1. Import GitHub repo into Zeabur
2. Use Dockerfile service (or `zeabur.json` scaffold)
3. Configure env vars/secrets in dashboard
