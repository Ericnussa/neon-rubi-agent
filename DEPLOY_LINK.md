# One-Link Deploy (Fastest)

## Click this:

## https://railway.com/deploy?repo=https://github.com/Ericnussa/neon-rubi-agent

Then set only these 3 values in Railway Variables:

1. `AUTH_SECRET` = any long random string
2. `ADMIN_PASSWORD` = your admin password
3. `OPENAI_API_KEY` **or** `ANTHROPIC_API_KEY`

Use default for:
- `ADMIN_USERNAME=admin`

After deploy:
- Open your Railway app URL
- Login with `admin` + your `ADMIN_PASSWORD`
