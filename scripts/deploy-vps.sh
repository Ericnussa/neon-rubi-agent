#!/usr/bin/env bash
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required. Install Docker first."
  exit 1
fi

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
  echo "Please edit .env (AUTH_SECRET, ADMIN_PASSWORD, API key), then re-run."
  exit 0
fi

docker compose up -d --build
echo "Deployed. Open http://SERVER_IP:8000"
