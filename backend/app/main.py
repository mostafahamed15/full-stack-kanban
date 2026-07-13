from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.db import ensure_db

app = FastAPI(title="Project Management MVP Backend")

ensure_db()

frontend_out = Path(__file__).resolve().parent.parent.parent / "frontend" / "out"


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/hello")
async def hello():
    return {"message": "hello from backend"}


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
