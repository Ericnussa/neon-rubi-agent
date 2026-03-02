#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "[1/5] Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "[2/5] Installing dependencies..."
pip install --upgrade pip >/dev/null
pip install -r requirements.txt >/dev/null

echo "[3/5] Preparing environment file..."
if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
else
  echo ".env already exists, leaving it unchanged"
fi

echo "[4/5] Running setup wizard..."
python scripts/setup_wizard.py

echo "[5/5] Installation complete"
echo "Run: source .venv/bin/activate && ./scripts/run-web.sh"
