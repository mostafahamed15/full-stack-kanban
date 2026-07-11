FROM python:3.12-slim

WORKDIR /app

RUN python -m pip install --no-cache-dir uv

COPY backend/pyproject.toml ./backend/pyproject.toml
COPY backend/app ./backend/app
COPY frontend/out ./frontend/out

WORKDIR /app/backend
RUN uv install

WORKDIR /app
EXPOSE 3000
CMD ["uv", "run", "backend.app.main:app", "--host", "0.0.0.0", "--port", "3000"]
