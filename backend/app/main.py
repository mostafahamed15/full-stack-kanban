import json
import os
import sys
import urllib.request
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

backend_root = Path(__file__).resolve().parent.parent
project_root = backend_root.parent
for candidate in (str(project_root), str(backend_root)):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

try:
    from backend.app.db import ensure_db, get_or_create_board, upsert_board
    from backend.app.schemas import BoardData
except ModuleNotFoundError:
    from app.db import ensure_db, get_or_create_board, upsert_board
    from app.schemas import BoardData

app = FastAPI(title="Project Management MVP Backend")

ensure_db()

frontend_out = Path(__file__).resolve().parent.parent.parent / "frontend" / "out"


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/hello")
async def hello():
    return {"message": "hello from backend"}


@app.get("/api/board", response_model=BoardData)
async def get_board(user_id: str = "user"):
    board = get_or_create_board(user_id)
    return board


@app.patch("/api/board", response_model=BoardData)
async def patch_board(board: BoardData, user_id: str = "user"):
    try:
        upsert_board(user_id, board.dict())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return board


@app.post("/api/ai/test")
async def ai_test(payload: dict):
    prompt = payload.get("prompt", "")
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY is not configured")

    request_body = {
        "model": "openai/gpt-oss-120b",
        "messages": [{"role": "user", "content": prompt}],
    }

    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "Project Management MVP",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    reply = payload.get("choices", [{}])[0].get("message", {}).get("content", "")
    return {"reply": reply, "model": "openai/gpt-oss-120b"}


if frontend_out.exists():
    app.mount("/_next", StaticFiles(directory=frontend_out / "_next"), name="next")
    if (frontend_out / "static").exists():
        app.mount("/static", StaticFiles(directory=frontend_out / "static"), name="static")


@app.get("/")
async def serve_index():
    return FileResponse(frontend_out / "index.html")


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    candidate = frontend_out / full_path
    if candidate.exists() and candidate.is_file():
        return FileResponse(candidate)
    return FileResponse(frontend_out / "index.html")
