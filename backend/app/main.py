from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.core.config import settings
from app.core.database import engine, Base
import app.models # registers models with Base.metadata

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.technologies import router as technologies_router
from app.api.v1.questions import router as questions_router
from app.api.v1.search import router as search_router
from app.api.v1.ai import router as ai_router
from app.api.v1.admin import router as admin_router
from app.api.v1.admin_content import router as admin_content_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize schema on startup (especially for SQLite or development environments)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Pre-warm high-traffic reading mode caches in background
    async def warm_cache():
        try:
            import asyncio
            from app.core.database import AsyncSessionLocal
            from app.services.question_service import QuestionService
            await asyncio.sleep(0.5)
            async with AsyncSessionLocal() as s:
                qs = QuestionService(s)
                for slug in ["langgraph", "java-backend", "rag-vector-db", "dsa", "system-design"]:
                    try:
                        await qs.get_reading_mode_data(slug)
                    except Exception:
                        pass
        except Exception:
            pass

    import asyncio
    asyncio.create_task(warm_cache())

    yield
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Technical Interview Preparation Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Compression Middleware - Compress responses larger than 1000 bytes
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Liveness and Readiness Probes
@app.get("/health", tags=["system"], status_code=status.HTTP_200_OK)
@app.get(f"{settings.API_V1_STR}/health", tags=["system"], status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok", "service": "Break The Code API"}

@app.get("/ready", tags=["system"], status_code=status.HTTP_200_OK)
async def readiness_check():
    return {
        "status": "ready",
        "database": "connected",
        "llm_provider": settings.LLM_PROVIDER
    }

# Wire v1 routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(technologies_router, prefix=settings.API_V1_STR)
app.include_router(questions_router, prefix=settings.API_V1_STR)
app.include_router(search_router, prefix=settings.API_V1_STR)
app.include_router(ai_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(admin_content_router, prefix=settings.API_V1_STR)

