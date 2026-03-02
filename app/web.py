from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.agent import AssistantAgent
from app.auth import require_admin
from app.config import Settings

app = FastAPI(title="Neon Rubi Agent")
settings = Settings()
agent = AssistantAgent()


class ChatRequest(BaseModel):
    message: str


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
      <h3>Admin Dashboard</h3>
      <p>Add your ADMIN_TOKEN below to view recent memory records.</p>
      <input id='tok' style='width:60%' placeholder='ADMIN_TOKEN' />
      <button id='load'>Load Recent Memories</button>
      <pre id='mem' style='white-space: pre-wrap; background:#1b1b1b; color:#9ef; padding:12px; min-height:180px;'></pre>

      <script>
        const f = document.getElementById('f');
        const out = document.getElementById('out');
        const mem = document.getElementById('mem');
        const load = document.getElementById('load');

        f.addEventListener('submit', async (e) => {
          e.preventDefault();
          const msg = document.getElementById('msg').value;
          const r = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({message: msg})});
          const j = await r.json();
          out.textContent += `you> ${msg}\nagent> ${j.reply}\n\n`;
        });

        load.addEventListener('click', async () => {
          const tok = document.getElementById('tok').value;
          const r = await fetch('/admin/memories', { headers: {'x-admin-token': tok} });
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


@app.get("/admin/memories")
def admin_memories(x_admin_token: str | None = Header(default=None)):
    require_admin(x_admin_token, settings.admin_token)
    return {"items": agent.memory.recent_memories(limit=50)}
