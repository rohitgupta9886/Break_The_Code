from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["search"])

@router.get("", response_model=Dict[str, Any])
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(15, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    service = SearchService(db)
    results = await service.hybrid_search(query=q, limit=limit)
    return {
        "success": True,
        "query": q,
        "count": len(results),
        "results": results
    }

@router.get("/autocomplete", response_model=Dict[str, Any])
async def autocomplete(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    service = SearchService(db)
    data = await service.autocomplete(query=q)
    return {
        "success": True,
        "query": q,
        "suggestions": data
    }
