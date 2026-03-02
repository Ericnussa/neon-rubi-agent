from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from app.db import get_conn, init_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def ensure_admin_user(db_path: Path, username: str, password: str) -> None:
    init_db(db_path)
    conn = get_conn(db_path)
    row = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    if not row:
        conn.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'admin')",
            (username, hash_password(password)),
        )
        conn.commit()
    conn.close()


def authenticate_user(db_path: Path, username: str, password: str) -> bool:
    conn = get_conn(db_path)
    row = conn.execute("SELECT password_hash FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if not row:
        return False
    return verify_password(password, row["password_hash"])


def create_access_token(secret: str, username: str, minutes: int = 60 * 24) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def require_bearer(token: str | None, secret: str) -> dict:
    if not token:
        raise HTTPException(status_code=401, detail="Missing bearer token")
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


def require_admin_token(x_admin_token: str | None, expected_token: str | None) -> None:
    if not expected_token:
        raise HTTPException(status_code=500, detail="ADMIN_TOKEN is not configured")
    if not x_admin_token or x_admin_token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
