from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from app.db import get_conn, init_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ROLE_LEVEL = {"viewer": 1, "editor": 2, "admin": 3}


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def ensure_user(db_path: Path, username: str, password: str, role: str = "viewer") -> None:
    init_db(db_path)
    conn = get_conn(db_path)
    row = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    if not row:
        conn.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, hash_password(password), role),
        )
        conn.commit()
    conn.close()


def create_user(db_path: Path, username: str, password: str, role: str) -> None:
    conn = get_conn(db_path)
    conn.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, hash_password(password), role),
    )
    conn.commit()
    conn.close()


def authenticate_user(db_path: Path, username: str, password: str) -> dict | None:
    conn = get_conn(db_path)
    row = conn.execute("SELECT username, password_hash, role FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if not row:
        return None
    if not verify_password(password, row["password_hash"]):
        return None
    return {"username": row["username"], "role": row["role"]}


def create_access_token(secret: str, username: str, role: str, minutes: int = 60 * 24) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "role": role,
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


def require_role(claims: dict, minimum_role: str) -> None:
    role = claims.get("role", "viewer")
    if ROLE_LEVEL.get(role, 0) < ROLE_LEVEL.get(minimum_role, 0):
        raise HTTPException(status_code=403, detail=f"Requires role: {minimum_role}")


def require_admin_token(x_admin_token: str | None, expected_token: str | None) -> None:
    if not expected_token:
        raise HTTPException(status_code=500, detail="ADMIN_TOKEN is not configured")
    if not x_admin_token or x_admin_token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
