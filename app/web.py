from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.agent import AssistantAgent
from app.auth import (
    authenticate_user,
    create_access_token,
    create_user,
    ensure_user,
    require_admin_token,
    require_bearer,
    require_role,
)
from app.chats import ChatStore
from app.config import Settings

app = FastAPI(title="Neon Rubi Agent")
settings = Settings()
ensure_user(settings.db_path, settings.admin_username, settings.admin_password, role="admin")
agent = AssistantAgent()
chats = ChatStore(settings.db_path)


class ChatRequest(BaseModel):
    message: str


class LoginRequest(BaseModel):
    username: str
    password: str


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str = "viewer"


class ThreadCreateRequest(BaseModel):
    title: str


class ThreadMessageRequest(BaseModel):
    role: str
    content: str


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return "<html><body><h2>Neon Rubi Agent</h2><p>API is running.</p></body></html>"


@app.post("/chat")
def chat(req: ChatRequest):
    return {"reply": agent.respond(req.message)}


@app.post("/auth/login")
def auth_login(req: LoginRequest):
    user = authenticate_user(settings.db_path, req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(settings.auth_secret, user["username"], user["role"])
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}


@app.post("/admin/users")
def admin_create_user(req: CreateUserRequest, authorization: str | None = Header(default=None)):
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    claims = require_bearer(token, settings.auth_secret)
    require_role(claims, "admin")
    if req.role not in {"admin", "editor", "viewer"}:
        raise HTTPException(status_code=400, detail="role must be admin|editor|viewer")
    create_user(settings.db_path, req.username, req.password, req.role)
    return {"ok": True, "username": req.username, "role": req.role}


@app.get("/admin/memories")
def admin_memories(x_admin_token: str | None = Header(default=None)):
    require_admin_token(x_admin_token, settings.admin_token)
    return {"items": agent.memory.recent_memories(limit=50)}


@app.get("/admin/memories-jwt")
def admin_memories_jwt(authorization: str | None = Header(default=None)):
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    claims = require_bearer(token, settings.auth_secret)
    require_role(claims, "viewer")
    return {"subject": claims.get("sub"), "role": claims.get("role"), "items": agent.memory.recent_memories(limit=50)}


@app.post("/threads")
def create_thread(req: ThreadCreateRequest, authorization: str | None = Header(default=None)):
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    claims = require_bearer(token, settings.auth_secret)
    require_role(claims, "editor")
    tid = chats.create_thread(req.title, claims.get("sub"))
    return {"thread_id": tid, "title": req.title}


@app.get("/threads")
def list_threads(authorization: str | None = Header(default=None)):
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    claims = require_bearer(token, settings.auth_secret)
    require_role(claims, "viewer")
    return {"items": chats.list_threads(limit=100)}


@app.post("/threads/{thread_id}/messages")
def add_thread_message(thread_id: int, req: ThreadMessageRequest, authorization: str | None = Header(default=None)):
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    claims = require_bearer(token, settings.auth_secret)
    require_role(claims, "editor")
    mid = chats.add_message(thread_id, req.role, req.content)
    return {"message_id": mid, "thread_id": thread_id}


@app.get("/threads/{thread_id}/messages")
def get_thread_messages(thread_id: int, authorization: str | None = Header(default=None)):
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    claims = require_bearer(token, settings.auth_secret)
    require_role(claims, "viewer")
    return {"items": chats.get_messages(thread_id, limit=500)}
