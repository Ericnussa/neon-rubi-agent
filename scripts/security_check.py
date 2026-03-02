#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"

BAD_DEFAULTS = {
    "AUTH_SECRET": {"", "change-this-secret"},
    "ADMIN_PASSWORD": {"", "change-me", "change-me-now"},
    "ADMIN_TOKEN": {"", "change-me"},
}


def parse_env(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.strip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


if __name__ == "__main__":
    env = parse_env(ENV_FILE)
    failed = []
    for key, disallowed in BAD_DEFAULTS.items():
        if env.get(key, "") in disallowed:
            failed.append(key)

    if failed:
        print("Security check FAILED. Fix these keys in .env:")
        for k in failed:
            print(f" - {k}")
        sys.exit(1)

    print("Security check passed.")
