FROM python:3.12-slim

WORKDIR /app

RUN python -m pip install --no-cache-dir fastapi uvicorn[standard]

COPY backend/app ./backend/app
COPY frontend/out ./frontend/out

WORKDIR /app
EXPOSE 3000
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "3000"]
