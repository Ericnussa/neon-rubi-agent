#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo "Bootstrap complete. Run: source .venv/bin/activate && python -m app.main"
