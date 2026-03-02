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


@app.get("/health")
def health():
    return {"ok": True, "service": "neon-rubi-agent"}


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Neon Rubi Agent</title>
  <style>
    :root { color-scheme: dark; }
    body { margin:0; font-family: Inter, system-ui, sans-serif; background:#0b0f17; color:#d7e3ff; }
    .app { display:grid; grid-template-columns: 320px 1fr; height:100vh; }
    .panel { border-right:1px solid #1d2640; padding:14px; overflow:auto; }
    .main { display:grid; grid-template-rows:auto 1fr auto; }
    .top { border-bottom:1px solid #1d2640; padding:12px 16px; display:flex; justify-content:space-between; align-items:center; }
    .threads, .admin { background:#10172a; border:1px solid #223158; border-radius:12px; padding:10px; margin-bottom:12px; }
    .threads h3, .admin h3 { margin:0 0 10px; font-size:14px; color:#8fb3ff; }
    .thread-item { padding:8px; border-radius:8px; background:#0f1628; margin-bottom:6px; cursor:pointer; border:1px solid transparent; }
    .thread-item:hover, .thread-item.active { border-color:#3f5faa; }
    .messages { padding:14px; overflow:auto; display:flex; flex-direction:column; gap:10px; }
    .msg { max-width:80%; padding:10px 12px; border-radius:12px; white-space:pre-wrap; }
    .msg.user { align-self:flex-end; background:#24408d; }
    .msg.assistant { align-self:flex-start; background:#1c2a4a; }
    .composer { border-top:1px solid #1d2640; padding:10px; display:flex; gap:8px; }
    input, select, button, textarea { background:#0f1628; color:#d7e3ff; border:1px solid #2a3c6d; border-radius:8px; padding:8px; }
    textarea { flex:1; min-height:44px; max-height:120px; resize:vertical; }
    button { cursor:pointer; }
    .row { display:flex; gap:8px; margin-bottom:8px; }
    .status { font-size:12px; color:#8fb3ff; }
    .hidden { display:none; }
  </style>
</head>
<body>
  <div class="app">
    <aside class="panel">
      <div class="threads">
        <h3>Login</h3>
        <div class="row"><input id="username" placeholder="username" style="flex:1"></div>
        <div class="row"><input id="password" type="password" placeholder="password" style="flex:1"></div>
        <div class="row"><button id="loginBtn">Login</button><button id="logoutBtn">Logout</button></div>
        <div id="me" class="status">Not logged in</div>
      </div>

      <div class="threads">
        <h3>Threads</h3>
        <div class="row"><input id="newThreadTitle" placeholder="New thread title" style="flex:1"><button id="newThreadBtn">Create</button></div>
        <div id="threadList"></div>
      </div>

      <div class="admin hidden" id="adminBox">
        <h3>Admin: Create User</h3>
        <div class="row"><input id="newUser" placeholder="username" style="flex:1"></div>
        <div class="row"><input id="newPass" placeholder="password" style="flex:1"></div>
        <div class="row">
          <select id="newRole"><option>viewer</option><option>editor</option><option>admin</option></select>
          <button id="createUserBtn">Create</button>
        </div>
      </div>
    </aside>

    <section class="main">
      <div class="top">
        <strong id="threadTitle">No thread selected</strong>
        <span class="status" id="status">Ready</span>
      </div>
      <div class="messages" id="messages"></div>
      <div class="composer">
        <textarea id="messageInput" placeholder="Type message..."></textarea>
        <button id="sendBtn">Send</button>
      </div>
    </section>
  </div>

<script>
let token = null;
let role = null;
let activeThreadId = null;

const $ = (id) => document.getElementById(id);

function setStatus(t){ $("status").textContent = t; }
function authHeaders(){ return token ? {"Authorization": `Bearer ${token}`} : {}; }

async function login(){
  const username = $("username").value;
  const password = $("password").value;
  const res = await fetch('/auth/login', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({username,password})});
  const data = await res.json();
  if(!res.ok){ setStatus(data.detail || 'Login failed'); return; }
  token = data.access_token; role = data.role;
  $("me").textContent = `Logged in as ${username} (${role})`;
  $("adminBox").classList.toggle('hidden', role !== 'admin');
  setStatus('Logged in');
  await loadThreads();
}

function logout(){ token=null; role=null; activeThreadId=null; $("me").textContent='Not logged in'; $("threadList").innerHTML=''; $("messages").innerHTML=''; $("threadTitle").textContent='No thread selected'; $("adminBox").classList.add('hidden'); }

async function loadThreads(){
  if(!token) return;
  const res = await fetch('/threads', {headers:authHeaders()});
  const data = await res.json();
  if(!res.ok){ setStatus(data.detail || 'Failed to load threads'); return; }
  const box = $("threadList"); box.innerHTML='';
  data.items.forEach(t => {
    const d = document.createElement('div');
    d.className = 'thread-item' + (t.id===activeThreadId?' active':'');
    d.textContent = `#${t.id} ${t.title}`;
    d.onclick = async () => { activeThreadId=t.id; $("threadTitle").textContent=t.title; await loadThreads(); await loadMessages(); };
    box.appendChild(d);
  });
}

async function createThread(){
  const title = $("newThreadTitle").value.trim();
  if(!title) return;
  const res = await fetch('/threads', {method:'POST', headers:{'Content-Type':'application/json', ...authHeaders()}, body:JSON.stringify({title})});
  const data = await res.json();
  if(!res.ok){ setStatus(data.detail || 'Failed to create thread'); return; }
  activeThreadId = data.thread_id;
  $("newThreadTitle").value='';
  await loadThreads();
  await loadMessages();
}

async function loadMessages(){
  if(!activeThreadId || !token) return;
  const res = await fetch(`/threads/${activeThreadId}/messages`, {headers:authHeaders()});
  const data = await res.json();
  if(!res.ok){ setStatus(data.detail || 'Failed to load messages'); return; }
  const box = $("messages"); box.innerHTML='';
  data.items.forEach(m => {
    const d = document.createElement('div');
    d.className = 'msg ' + (m.role === 'user' ? 'user' : 'assistant');
    d.textContent = m.content;
    box.appendChild(d);
  });
  box.scrollTop = box.scrollHeight;
}

async function sendMessage(){
  const content = $("messageInput").value.trim();
  if(!content || !activeThreadId || !token) return;

  const saveUser = await fetch(`/threads/${activeThreadId}/messages`, {method:'POST', headers:{'Content-Type':'application/json', ...authHeaders()}, body:JSON.stringify({role:'user', content})});
  const saveUserData = await saveUser.json();
  if(!saveUser.ok){ setStatus(saveUserData.detail || 'Failed to save message'); return; }

  const chatRes = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message:content})});
  const chatData = await chatRes.json();

  await fetch(`/threads/${activeThreadId}/messages`, {method:'POST', headers:{'Content-Type':'application/json', ...authHeaders()}, body:JSON.stringify({role:'assistant', content:chatData.reply || ''})});

  $("messageInput").value='';
  await loadMessages();
}

async function createUser(){
  const username = $("newUser").value.trim();
  const password = $("newPass").value.trim();
  const roleV = $("newRole").value;
  if(!username || !password) return;
  const res = await fetch('/admin/users', {method:'POST', headers:{'Content-Type':'application/json', ...authHeaders()}, body:JSON.stringify({username,password,role:roleV})});
  const data = await res.json();
  setStatus(res.ok ? `Created ${data.username} (${data.role})` : (data.detail || 'Failed to create user'));
}

$("loginBtn").onclick = login;
$("logoutBtn").onclick = logout;
$("newThreadBtn").onclick = createThread;
$("sendBtn").onclick = sendMessage;
$("createUserBtn").onclick = createUser;
</script>
</body>
</html>
"""


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
