# 🐳 Docker Deployment & Architecture Guide

This project is fully dockerized with a production-grade multi-container architecture using Docker Compose.

---

## 🏗️ Architecture Overview

The multi-container setup consists of 4 isolated services connected via the internal `btc_network` bridge network:

| Service | Technology / Base Image | Host:Container Port | Description |
| :--- | :--- | :--- | :--- |
| **`btc_frontend`** | Next.js 15 Standalone (`node:20-alpine`) | `3000:3000` | Multi-stage production build running as non-root user `nextjs`. |
| **`btc_backend`** | FastAPI (`python:3.12-slim`) | `8001:8000` | High-performance Python backend with Uvicorn, GZip compression, and SQLite/PostgreSQL support. |
| **`btc_postgres`** | `pgvector/pgvector:pg16` | `5434:5432` | PostgreSQL 16 with pgvector extension enabled for vector similarity search. |
| **`btc_redis`** | `redis:7.2-alpine` | `6380:6379` | In-memory cache and session store with automatic ping health checks. |

---

## 🚀 Quick Start

### 1. Prerequisites
- Docker Engine & Docker Desktop installed ([Get Docker](https://docs.docker.com/get-docker/))
- Ensure Docker Desktop is running

### 2. Configure Environment (Optional)
If you have custom environment variables or AI keys (e.g. Gemini), ensure they are in `.env` in the project root:
```bash
# Example .env additions
LLM_PROVIDER=gemini
LLM_API_KEY=your_gemini_api_key_here
```

### 3. Build & Run
Run all services with a single command:
```bash
docker compose up --build -d
```

### 4. Verify Services
- **Frontend Web UI**: [http://localhost:3000](http://localhost:3000)
- **Backend API Docs (Swagger UI)**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **Backend Health Check**: [http://localhost:8001/health](http://localhost:8001/health)
- **Backend Readiness Check**: [http://localhost:8001/ready](http://localhost:8001/ready)

---

## 🛠️ Common Docker Commands

### View Logs
Stream live logs across all containers:
```bash
docker compose logs -f
```

Or view logs for a specific service:
```bash
docker compose logs -f backend
docker compose logs -f frontend
```

### Check Container Status & Health
```bash
docker compose ps
```

### Stop Containers
```bash
docker compose down
```

### Stop Containers & Wipe Data Volumes
```bash
docker compose down -v
```

### Rebuild a Specific Service
If you made changes to the backend or frontend and only want to rebuild that container:
```bash
docker compose up -d --build backend
docker compose up -d --build frontend
```

---

## 💡 Dual-Database Mode (SQLite vs PostgreSQL)

- **Default (Plug-and-play)**: The backend is pre-configured to automatically fallback to `sqlite+aiosqlite:///./breakthecode.db` which includes the populated questions and seed data.
- **Production PostgreSQL**: To switch to PostgreSQL, set in your `.env`:
  ```bash
  DATABASE_URL=postgresql+asyncpg://btc_user:btc_password@postgres:5432/breakthecode
  SYNC_DATABASE_URL=postgresql://btc_user:btc_password@postgres:5432/breakthecode
  ```
