from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from app.core.database import get_db
from app.models.question import Question
from app.models.taxonomy import Technology
from app.models.source import ContentSource
from app.models.audit import ContentGenerationJob, AuditLog
from app.services.content_pipeline import DIFFICULTY_TIERS

router = APIRouter(prefix="/admin/content", tags=["admin-content"])

class GenerateJobRequest(BaseModel):
    technology_slug: str
    target_difficulty: str
    target_count: int = 30

@router.get("/matrix", response_model=Dict[str, Any])
async def get_coverage_matrix(db: AsyncSession = Depends(get_db)):
    """
    Returns the real-time 8xN Technology Coverage Matrix with live counts,
    satisfying the admin coverage requirements.
    """
    techs = (await db.execute(select(Technology).order_by(Technology.order_index))).scalars().all()
    matrix_rows = []

    all_tiers = [d["tier"] for d in DIFFICULTY_TIERS]

    for tech in techs:
        row = {
            "technology_id": tech.id,
            "technology_name": tech.name,
            "technology_slug": tech.slug,
            "counts": {},
            "total": 0,
            "is_fully_covered": True
        }
        tech_total = 0
        for tier in all_tiers:
            count = await db.scalar(
                select(func.count(Question.id))
                .where(Question.technology_id == tech.id, Question.difficulty == tier)
            )
            row["counts"][tier] = count
            tech_total += count
            if count < 30:
                row["is_fully_covered"] = False
        row["total"] = tech_total
        matrix_rows.append(row)

    return {
        "success": True,
        "difficulty_tiers": DIFFICULTY_TIERS,
        "matrix": matrix_rows
    }

@router.get("/gaps", response_model=Dict[str, Any])
async def get_content_gaps(db: AsyncSession = Depends(get_db)):
    """Identifies technology sections with fewer than 30 questions in any difficulty tier."""
    techs = (await db.execute(select(Technology))).scalars().all()
    all_tiers = [d["tier"] for d in DIFFICULTY_TIERS]
    gaps = []

    for tech in techs:
        for tier in all_tiers:
            count = await db.scalar(
                select(func.count(Question.id))
                .where(Question.technology_id == tech.id, Question.difficulty == tier)
            )
            if count < 30:
                gaps.append({
                    "technology_name": tech.name,
                    "technology_slug": tech.slug,
                    "difficulty": tier,
                    "current_count": count,
                    "target_count": 30,
                    "missing_count": 30 - count
                })

    return {
        "success": True,
        "total_gaps": len(gaps),
        "gaps": gaps
    }

@router.get("/sources", response_model=Dict[str, Any])
async def list_content_sources(db: AsyncSession = Depends(get_db)):
    """Returns the registry of verified primary and official documentation sources."""
    sources = (await db.execute(select(ContentSource).order_by(ContentSource.created_at.desc()))).scalars().all()
    return {
        "success": True,
        "total": len(sources),
        "items": [
            {
                "id": s.id,
                "title": s.title,
                "url": s.url,
                "source_type": s.source_type,
                "publisher": s.publisher,
                "technology": s.technology,
                "trust_level": s.trust_level,
                "last_verified_at": s.last_verified_at
            }
            for s in sources
        ]
    }
