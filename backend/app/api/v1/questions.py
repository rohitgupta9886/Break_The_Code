from typing import List, Optional, Any, Dict, Tuple
from fastapi import APIRouter, Depends, Query, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.api.deps import get_current_user, get_current_active_user
from app.models.user import User
from app.models.question import Question, QuestionRelation
from app.models.taxonomy import Technology
from app.services.question_service import QuestionService
from app.schemas.question import (
    QuestionFilterParams,
    QuestionCardSchema,
    QuestionDetailSchema,
    QuestionHintSchema
)

router = APIRouter(prefix="/questions", tags=["questions"])

_STATS_CACHE: Optional[Tuple[Dict[str, Any], float]] = None
_STATS_CACHE_TTL = 60.0

@router.get("/stats", response_model=Dict[str, Any])
async def get_question_stats(response: Response, db: AsyncSession = Depends(get_db)):
    """Returns live count statistics across all 8 difficulty tiers and technology tracks."""
    import time
    global _STATS_CACHE
    now = time.time()
    if _STATS_CACHE and (now - _STATS_CACHE[1] < _STATS_CACHE_TTL):
        response.headers["Cache-Control"] = "public, max-age=60, stale-while-revalidate=180"
        return _STATS_CACHE[0]

    from sqlalchemy import and_
    total = await db.scalar(select(func.count(Question.id)).where(Question.status == "PUBLISHED"))
    
    # Counts by Difficulty
    diff_counts = {}
    diff_query = await db.execute(
        select(Question.difficulty, func.count(Question.id))
        .where(Question.status == "PUBLISHED")
        .group_by(Question.difficulty)
    )
    for diff, count in diff_query.all():
        diff_counts[diff] = count

    # Counts by Technology (Single Join Query, Zero N+1)
    tech_counts = {}
    tech_query = await db.execute(
        select(Technology.slug, Technology.name, func.count(Question.id))
        .outerjoin(Question, and_(Question.technology_id == Technology.id, Question.status == "PUBLISHED"))
        .where(Technology.is_active == True)
        .group_by(Technology.id)
    )
    for slug, name, count in tech_query.all():
        tech_counts[slug] = {
            "name": name,
            "count": count
        }

    res_data = {
        "success": True,
        "total_questions": total,
        "by_difficulty": diff_counts,
        "by_technology": tech_counts,
    }
    _STATS_CACHE = (res_data, now)
    response.headers["Cache-Control"] = "public, max-age=60, stale-while-revalidate=180"
    return res_data

@router.get("/difficulty/{difficulty}", response_model=Dict[str, Any])
async def list_questions_by_difficulty(
    difficulty: str,
    technology: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Direct route for difficulty-filtered questions."""
    service = QuestionService(db)
    params = QuestionFilterParams(
        difficulty=difficulty.upper(),
        technology=technology,
        page=page,
        limit=limit
    )
    cards, total = await service.list_questions(params)
    return {
        "success": True,
        "difficulty": difficulty.upper(),
        "items": cards,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit if limit > 0 else 1
    }

@router.get("/technology/{technology}", response_model=Dict[str, Any])
async def list_questions_by_technology(
    technology: str,
    difficulty: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    service = QuestionService(db)
    params = QuestionFilterParams(
        technology=technology,
        difficulty=difficulty.upper() if difficulty else None,
        page=page,
        limit=limit
    )
    cards, total = await service.list_questions(params)
    return {
        "success": True,
        "technology": technology,
        "items": cards,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit if limit > 0 else 1
    }

@router.get("/technology/{technology}/difficulty/{difficulty}", response_model=Dict[str, Any])
async def list_questions_by_tech_and_diff(
    technology: str,
    difficulty: str,
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    service = QuestionService(db)
    params = QuestionFilterParams(
        technology=technology,
        difficulty=difficulty.upper(),
        page=page,
        limit=limit
    )
    cards, total = await service.list_questions(params)
    return {
        "success": True,
        "technology": technology,
        "difficulty": difficulty.upper(),
        "items": cards,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit if limit > 0 else 1
    }

@router.get("", response_model=Dict[str, Any])
async def list_questions(
    technology: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    interview_depth: Optional[str] = Query(None),
    question_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    service = QuestionService(db)
    params = QuestionFilterParams(
        technology=technology,
        topic=topic,
        difficulty=difficulty,
        interview_depth=interview_depth,
        question_type=question_type,
        search=search,
        page=page,
        limit=limit
    )
    cards, total = await service.list_questions(params)
    return {
        "success": True,
        "items": cards,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit if limit > 0 else 1
    }

from fastapi.responses import JSONResponse

@router.get("/reading-mode/{technology_slug}")
async def get_reading_mode_qa(
    technology_slug: str,
    response: Response,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Dedicated Q&A Reading Mode endpoint.
    Returns all published questions with full answers for a technology track,
    grouped by validated difficulty tier and ordered deterministically for continuous single-page reading.
    """
    service = QuestionService(db)
    data = await service.get_reading_mode_data(technology_slug, current_user.id if current_user else None)
    return JSONResponse(
        content=data,
        headers={"Cache-Control": "public, max-age=180, stale-while-revalidate=600"}
    )

@router.get("/{slug}", response_model=Dict[str, Any])
async def get_question_detail(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    service = QuestionService(db)
    q = await service.get_by_slug(slug)
    
    is_bookmarked = False
    if current_user:
        is_bookmarked = await service.question_repo.is_bookmarked(current_user.id, q.id)

    data = {
        "id": q.id,
        "slug": q.slug,
        "title": q.title,
        "difficulty": q.difficulty,
        "difficulty_score": getattr(q, "difficulty_score", 5.0),
        "interview_depth": q.interview_depth,
        "question_type": q.question_type,
        "scenario_type": getattr(q, "scenario_type", None),
        "role_target": q.role_target,
        "experience_level": q.experience_level,
        "interview_round": getattr(q, "interview_round", "Technical Screen"),
        "estimated_time_minutes": q.estimated_time_minutes,
        "short_answer": q.short_answer,
        "interview_ready_answer": q.interview_ready_answer,
        "deep_explanation": q.deep_explanation,
        "architecture_notes": q.architecture_notes,
        "code_example": q.code_example,
        "why_interviewer_asks": getattr(q, "why_interviewer_asks", None),
        "interviewer_intent": q.interviewer_intent,
        "production_considerations": getattr(q, "production_considerations", None),
        "failure_modes": getattr(q, "failure_modes", None),
        "tradeoffs": getattr(q, "tradeoffs", None),
        "common_mistakes": q.common_mistakes or [],
        "status": q.status,
        "content_origin": q.content_origin,
        "technology_version": getattr(q, "technology_version", "Current (2026)"),
        "technical_accuracy_score": getattr(q, "technical_accuracy_score", 0.95),
        "overall_quality_score": getattr(q, "overall_quality_score", 0.94),
        "view_count": q.view_count,
        "upvote_count": q.upvote_count,
        "created_at": q.created_at,
        "last_reviewed_at": q.last_reviewed_at,
        "technology_name": q.technology.name if q.technology else None,
        "technology_slug": q.technology.slug if q.technology else None,
        "topic_name": q.topic.name if q.topic else None,
        "is_bookmarked": is_bookmarked,
        "hints": [
            {
                "id": h.id,
                "hint_level": h.hint_level,
                "hint_type": h.hint_type,
                "content": h.content
            } for h in q.hints
        ],
        "sources": [
            {
                "source_name": s.source_name,
                "source_url": s.source_url,
                "license": s.license,
                "attribution_required": s.attribution_required
            } for s in q.sources
        ],
        "followups": [
            {
                "id": f.id,
                "followup_question": f.followup_question,
                "answer_guidance": f.answer_guidance
            } for f in q.followups
        ],
        "tags": [{"name": t.name, "slug": t.slug} for t in q.tags]
    }
    return {"success": True, "data": data}

@router.post("/{id}/bookmark", response_model=Dict[str, Any])
async def toggle_bookmark(
    id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    service = QuestionService(db)
    bookmarked = await service.toggle_bookmark(current_user.id, id)
    return {
        "success": True,
        "bookmarked": bookmarked,
        "message": "Question bookmarked" if bookmarked else "Bookmark removed"
    }
