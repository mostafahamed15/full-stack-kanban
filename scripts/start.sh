#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
cd backend
python -m uv run uvicorn app.main:app --reload --port 3000
