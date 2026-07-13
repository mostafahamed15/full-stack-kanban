# Project Management MVP Backend

This backend serves the static frontend and exposes API endpoints for the MVP.

## Run locally

```powershell
cd e:\AI-coder\pm\frontend
npm install
npm run build
cd ..
python -m uv run backend.app.main --reload --port 3000
```

## Run with scripts

- Windows: `scripts\start.ps1`
- macOS/Linux: `scripts/start.sh`

## Docker

Build and run the container from the repo root:

```powershell
docker build -t pm-backend .
docker run --rm -p 3000:3000 pm-backend
```

The Dockerfile now builds the Next.js frontend and copies the generated `frontend/out` static export into the runtime image.

## Endpoints

- `GET /` - serves the static frontend from `frontend/out`
- `GET /api/health` - health check endpoint
- `GET /api/hello` - simple backend hello endpoint

## Tests

Run backend route tests:

```powershell
python -m unittest discover -s backend/tests
```
