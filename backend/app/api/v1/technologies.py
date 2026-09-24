import time
from typing import List, Optional, Tuple, Any
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.taxonomy_repo import TaxonomyRepository
from app.schemas.taxonomy import TechnologyBase, DomainWithTechnologies

router = APIRouter(prefix="/technologies", tags=["technologies"])

_TECH_CACHE: Optional[Tuple[List[dict], float]] = None
_TECH_CACHE_TTL = 120.0 # 2 minutes

def invalidate_technology_cache():
    global _TECH_CACHE
    _TECH_CACHE = None

@router.get("", response_model=List[TechnologyBase])
async def list_technologies(response: Response, db: AsyncSession = Depends(get_db)):
    global _TECH_CACHE
    now = time.time()
    if _TECH_CACHE and (now - _TECH_CACHE[1] < _TECH_CACHE_TTL):
        response.headers["Cache-Control"] = "public, max-age=120, stale-while-revalidate=300"
        return _TECH_CACHE[0]

    repo = TaxonomyRepository(db)
    tech_counts = await repo.list_technologies_with_counts()
    
    result = []
    for t, count in tech_counts:
        result.append(
            TechnologyBase(
                id=t.id,
                name=t.name,
                slug=t.slug,
                short_description=t.short_description,
                icon=t.icon,
                is_active=t.is_active,
                order_index=t.order_index,
                question_count=count,
                topics=[
                    {
                        "id": top.id,
                        "name": top.name,
                        "slug": top.slug,
                        "description": top.description,
                        "order_index": top.order_index
                    } for top in t.topics
                ]
            )
        )
    _TECH_CACHE = (result, now)
    response.headers["Cache-Control"] = "public, max-age=120, stale-while-revalidate=300"
    return result

@router.get("/{slug}", response_model=TechnologyBase)
async def get_technology_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    repo = TaxonomyRepository(db)
    t = await repo.get_technology_by_slug(slug)
    if not t:
        raise HTTPException(status_code=404, detail="Technology not found")
    count = await repo.get_question_count_by_tech(t.id)
    return TechnologyBase(
        id=t.id,
        name=t.name,
        slug=t.slug,
        short_description=t.short_description,
        icon=t.icon,
        is_active=t.is_active,
        order_index=t.order_index,
        question_count=count,
        topics=[
            {
                "id": top.id,
                "name": top.name,
                "slug": top.slug,
                "description": top.description,
                "order_index": top.order_index
            } for top in t.topics
        ]
    )
