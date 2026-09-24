# Deployment & Infrastructure Guide (DEPLOYMENT.md)
## Break The Code — DevOps & Orchestration

---

## 1. Local Development Stack (Docker Compose)

```yaml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: btc_postgres
    environment:
      POSTGRES_USER: btc_user
      POSTGRES_PASSWORD: btc_password
      POSTGRES_DB: breakthecode
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U btc_user -d breakthecode"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7.2-alpine
    container_name: btc_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: btc_backend
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: btc_frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
```

---

## 2. Environment Variables (.env)
```bash
# Core Application
ENVIRONMENT=development
SECRET_KEY=supersecretjwtkeyforbreakthecode2026productiongrade
JWT_SECRET=supersecretjwtkeyforbreakthecode2026productiongrade
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database
DATABASE_URL=postgresql+asyncpg://btc_user:btc_password@localhost:5432/breakthecode
SYNC_DATABASE_URL=postgresql://btc_user:btc_password@localhost:5432/breakthecode

# Redis
REDIS_URL=redis://localhost:6379/0

# AI Provider Configuration
LLM_PROVIDER=mock # or openai, anthropic, gemini
LLM_API_KEY=
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=break-the-code
```

---

## 3. Production Health Endpoints
- `/health`: Liveness probe (returns 200 OK if service process is running).
- `/ready`: Readiness probe (verifies PostgreSQL connection and Redis ping).
