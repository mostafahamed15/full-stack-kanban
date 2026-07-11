#!/usr/bin/env bash
set -e
pkill -f "uv run backend/app/main.py" || true
