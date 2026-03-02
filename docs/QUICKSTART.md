# Quickstart (Non-Developers)

## 1) Download

- Open: https://github.com/Ericnussa/neon-rubi-agent
- Click **Code → Download ZIP**
- Extract it

## 2) Install

From the project folder:

```bash
./scripts/install.sh
```

This creates a virtual environment, installs dependencies, and runs a setup wizard.

## 3) Start

```bash
source .venv/bin/activate
./scripts/run-web.sh
```

Open your browser to: `http://127.0.0.1:8000`

## 4) Login

Use the admin username/password you set in setup wizard.

---

If the app says API keys are missing, add one (OpenAI or Anthropic) in `.env`.
