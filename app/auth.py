from fastapi import Header, HTTPException


def require_admin(x_admin_token: str | None, expected_token: str | None) -> None:
    if not expected_token:
        raise HTTPException(status_code=500, detail="ADMIN_TOKEN is not configured")
    if not x_admin_token or x_admin_token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
