# Project Management MVP Backend

This backend serves the static frontend and exposes API endpoints for the MVP.

## Run locally

```powershell
cd e:\AI-coder\pm
.\backend\.venv\Scripts\python -m uvicorn backend.app.main:app --reload --port 3000
```

## Run with scripts

- Windows: `scripts\start.ps1`
- macOS/Linux: `scripts/start.sh`

## Endpoints

- `GET /` - serves the static frontend from `frontend/out`
- `GET /api/health` - health check endpoint
- `GET /api/hello` - simple backend hello endpoint
