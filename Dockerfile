FROM node:20-alpine AS frontend-build

WORKDIR /build
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/tsconfig.json frontend/next.config.ts frontend/postcss.config.mjs frontend/next-env.d.ts ./
COPY frontend/public ./public
COPY frontend/src ./src
RUN npm run build

FROM python:3.12-slim AS runtime

WORKDIR /app
RUN python -m pip install --no-cache-dir fastapi uvicorn[standard]
COPY backend/app ./backend/app
COPY --from=frontend-build /build/out ./frontend/out
EXPOSE 3000
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "3000"]
