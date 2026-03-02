from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.agent import AssistantAgent

app = FastAPI(title="Neon Rubi Agent")
agent = AssistantAgent()


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """
    <html><body style='font-family: sans-serif; max-width: 700px; margin: 40px auto;'>
      <h2>Neon Rubi Agent</h2>
      <form id='f'>
        <input id='msg' style='width:80%' placeholder='Say something...' />
        <button>Send</button>
      </form>
      <pre id='out' style='white-space: pre-wrap; background:#111; color:#0f0; padding:12px;'></pre>
      <script>
        const f = document.getElementById('f');
        const out = document.getElementById('out');
        f.addEventListener('submit', async (e) => {
          e.preventDefault();
          const msg = document.getElementById('msg').value;
          const r = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({message: msg})});
          const j = await r.json();
          out.textContent += `you> ${msg}\nagent> ${j.reply}\n\n`;
        });
      </script>
    </body></html>
    """


@app.post("/chat")
def chat(req: ChatRequest):
    return {"reply": agent.respond(req.message)}
