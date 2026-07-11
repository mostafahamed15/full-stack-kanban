#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python -m uv run backend/app/main.py --reload --port 3000
