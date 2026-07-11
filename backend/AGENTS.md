# Backend AGENTS.md

## Purpose

This document describes the backend architecture for the Project Management MVP.

## Current backend state

- FastAPI application in `backend/app/main.py`.
- Serves an exported frontend from `frontend/out`.
- Provides API endpoints:
  - `GET /api/health`
  - `GET /api/hello`
- Backend runtime can be managed locally using `backend/.venv`.
- Includes Docker support and run scripts.

## What is implemented in Part 2

- Backend skeleton with FastAPI.
- Local run scripts in `scripts/` for Windows and macOS/Linux.
- Dockerfile scaffold to build the backend image.
- Static frontend serving from the exported Next.js app.
- Basic backend README documentation.

## Current limitations

- No database or persistence layer.
- No auth or session handling.
- No backend unit tests yet.
- Docker build has not been validated in this environment.

## Next backend work

- Add SQLite persistence and create database schema.
- Add board read/write API routes and user scoping.
- Integrate frontend with backend API.
- Add OpenRouter AI connectivity and structured output handling.
