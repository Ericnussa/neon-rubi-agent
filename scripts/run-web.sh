#!/usr/bin/env bash
set -euo pipefail
source .venv/bin/activate
uvicorn app.web:app --host "${HOST:-127.0.0.1}" --port "${PORT:-8000}" --reload
