from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.agent import AssistantAgent
from app.auth import (
    authenticate_user,
    create_access_token,
    ensure_admin_user,
    require_admin_token,
    require_bearer,
)
from app.config import Settings

app = FastAPI(title="Neon Rubi Agent")
settings = Settings()
ensure_admin_user(settings.db_path, settings.admin_username, settings.admin_password)
agent = AssistantAgent()


class ChatRequest(BaseModel):
    message: str


class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """
    <html><body style='font-family: sans-serif; max-width: 900px; margin: 40px auto;'>
      <h2>Neon Rubi Agent</h2>
      <form id='f'>
        <input id='msg' style='width:80%' placeholder='Say something...' />
        <button>Send</button>
      </form>
      <pre id='out' style='white-space: pre-wrap; background:#111; color:#0f0; padding:12px; min-height:180px;'></pre>
      <hr/>
      <h3>Admin Login (JWT)</h3>
      <input id='user' placeholder='username' />
      <input id='pass' type='password' placeholder='password' />
      <button id='login'>Login</button>
      <p><small>Token saved in browser memory only for this tab.</small></p>
      <button id='load'>Load Recent Memories (JWT)</button>
      <pre id='mem' style='white-space: pre-wrap; background:#1b1b1b; color:#9ef; padding:12px; min-height:180px;'></pre>

      <script>
        let jwtToken = null;
        const f = document.getElementById('f');
        const out = document.getElementById('out');
        const mem = document.getElementById('mem');
        const login = document.getElementById('login');
        const load = document.getElementById('load');

        f.addEventListener('submit', async (e) => {
          e.preventDefault();
          const msg = document.getElementById('msg').value;
          const r = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({message: msg})});
          const j = await r.json();
          out.textContent += `you> ${msg}\nagent> ${j.reply}\n\n`;
        });

        login.addEventListener('click', async () => {
          const username = document.getElementById('user').value;
          const password = document.getElementById('pass').value;
          const r = await fetch('/auth/login', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username, password})});
          const j = await r.json();
          if (j.access_token) {
            jwtToken = j.access_token;
            mem.textContent = 'Login successful. JWT loaded.';
          } else {
            mem.textContent = `Login failed: ${j.detail || 'unknown error'}`;
          }
        });

        load.addEventListener('click', async () => {
          if (!jwtToken) {
            mem.textContent = 'Login first.';
            return;
          }
          const r = await fetch('/admin/memories-jwt', { headers: {'Authorization': `Bearer ${jwtToken}` } });
          const j = await r.json();
          if (j.detail) {
            mem.textContent = `Error: ${j.detail}`;
            return;
          }
          mem.textContent = JSON.stringify(j, null, 2);
        });
      </script>
    </body></html>
    """


@app.post("/chat")
def chat(req: ChatRequest):
    return {"reply": agent.respond(req.message)}


@app.post("/auth/login")
def auth_login(req: LoginRequest):
    if not authenticate_user(settings.db_path, req.username, req.password):
        return {"detail": "Invalid credentials"}
    token = create_access_token(settings.auth_secret, req.username)
    return {"access_token": token, "token_type": "bearer"}


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
    return {"subject": claims.get("sub"), "items": agent.memory.recent_memories(limit=50)}
