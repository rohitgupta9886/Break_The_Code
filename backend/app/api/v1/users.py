from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.interaction import Bookmark, UserAttempt, UserProgress, SpacedRepetitionCard, UserBadge
from app.models.question import Question
from app.models.taxonomy import Technology, Topic
from app.services.srs_service import SRSService
from app.services.gamification_service import BADGE_CATALOG
from app.schemas.user import (
    UserRead,
    DashboardResponse,
    BadgeRead,
    SRSCardRead,
    SRSReviewRequest,
    TechProgressItem,
    RecentAttemptItem
)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    level = (current_user.xp // 200) + 1
    user_data = UserRead(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        avatar_url=current_user.avatar_url,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        xp=current_user.xp,
        streak_days=current_user.streak_days,
        level=level,
        roles=current_user.roles or [],
        created_at=current_user.created_at
    )
    return user_data

@router.get("/dashboard", response_model=DashboardResponse)
async def get_user_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # SQL Aggregations for fast dashboard loading
    total_attempted = (await db.scalar(
        select(func.count(UserAttempt.id)).where(UserAttempt.user_id == current_user.id)
    )) or 0
    total_completed = (await db.scalar(
        select(func.count(UserAttempt.id)).where(
            UserAttempt.user_id == current_user.id,
            UserAttempt.score_overall >= 7.0
        )
    )) or 0
    avg_score = (await db.scalar(
        select(func.avg(UserAttempt.score_overall)).where(UserAttempt.user_id == current_user.id)
    )) or 0.0
    overall_accuracy = round(avg_score * 10.0, 1)

    # Fetch ONLY the 5 most recent attempts
    stmt_recent = (
        select(UserAttempt)
        .where(UserAttempt.user_id == current_user.id)
        .options(
            selectinload(UserAttempt.question).selectinload(Question.technology)
        )
        .order_by(desc(UserAttempt.created_at))
        .limit(5)
    )
    res_recent = await db.execute(stmt_recent)
    recent_attempts_rows = list(res_recent.scalars().all())

    # XP & Level Calculation
    xp = current_user.xp
    level = (xp // 200) + 1
    current_level_base = (level - 1) * 200
    level_progress_xp = xp - current_level_base
    current_level_progress_pct = round(min(100.0, (level_progress_xp / 200.0) * 100.0), 1)

    # Technologies progress
    tech_stmt = select(Technology).order_by(Technology.order_index)
    all_techs = (await db.execute(tech_stmt)).scalars().all()

    prog_stmt = select(UserProgress).where(UserProgress.user_id == current_user.id)
    user_progs = {p.technology_id: p for p in (await db.execute(prog_stmt)).scalars().all()}

    tech_progress_items: List[TechProgressItem] = []
    for t in all_techs:
        p = user_progs.get(t.id)
        tech_progress_items.append(TechProgressItem(
            technology_id=t.id,
            name=t.name,
            slug=t.slug,
            icon=t.icon or "Code",
            attempted=p.questions_attempted if p else 0,
            completed=p.questions_completed if p else 0,
            accuracy_rate=p.accuracy_rate if p else 0.0
        ))

    # Recent attempts (last 5)
    recent_attempts: List[RecentAttemptItem] = []
    for a in recent_attempts_rows:
        q = a.question
        if q:
            recent_attempts.append(RecentAttemptItem(
                id=a.id,
                question_id=q.id,
                question_title=q.title,
                question_slug=q.slug,
                technology_name=q.technology.name if q.technology else "General",
                difficulty=q.difficulty,
                score=a.score_overall,
                xp_earned=a.xp_earned,
                time_spent_seconds=a.time_spent_seconds,
                created_at=a.created_at
            ))

    # Spaced Repetition due count
    now = datetime.utcnow()
    srs_count_stmt = select(func.count(SpacedRepetitionCard.id)).where(
        SpacedRepetitionCard.user_id == current_user.id,
        SpacedRepetitionCard.next_review_at <= now
    )
    revision_due_count = (await db.execute(srs_count_stmt)).scalar_one_or_none() or 0

    # Badges
    badge_stmt = select(UserBadge).where(UserBadge.user_id == current_user.id)
    earned_badges = {b.badge_key: b for b in (await db.execute(badge_stmt)).scalars().all()}

    badges_list: List[BadgeRead] = []
    for catalog_badge in BADGE_CATALOG:
        key = catalog_badge["badge_key"]
        earned = earned_badges.get(key)
        badges_list.append(BadgeRead(
            badge_key=key,
            badge_name=catalog_badge["badge_name"],
            badge_description=catalog_badge["badge_description"],
            icon=catalog_badge["icon"],
            is_unlocked=earned is not None,
            unlocked_at=earned.unlocked_at if earned else None
        ))

    # Weak topics identification
    weak_topics = []
    low_accuracy_techs = [tp for tp in tech_progress_items if tp.attempted > 0 and tp.accuracy_rate < 75.0]
    for lat in low_accuracy_techs:
        weak_topics.append(lat.name)
    if not weak_topics:
        weak_topics = ["Distributed Systems & Consensus", "Advanced Cache Invalidation"]

    # Daily challenge question
    attempted_qids = {a.question_id for a in attempts}
    unattempted_stmt = (
        select(Question)
        .options(selectinload(Question.technology))
        .where(Question.id.not_in(attempted_qids) if attempted_qids else True)
        .limit(1)
    )
    daily_q = (await db.execute(unattempted_stmt)).scalars().first()
    if not daily_q:
        first_q_stmt = select(Question).options(selectinload(Question.technology)).limit(1)
        daily_q = (await db.execute(first_q_stmt)).scalars().first()

    daily_challenge = None
    if daily_q:
        daily_challenge = {
            "id": daily_q.id,
            "title": daily_q.title,
            "slug": daily_q.slug,
            "difficulty": daily_q.difficulty,
            "technology_name": daily_q.technology.name if daily_q.technology else "AI",
            "estimated_time_minutes": daily_q.estimated_time_minutes,
            "reward_xp": 100
        }

    return DashboardResponse(
        total_attempted=total_attempted,
        total_completed=total_completed,
        overall_accuracy=overall_accuracy,
        total_xp=xp,
        level=level,
        xp_for_next_level=level * 200,
        current_level_progress_pct=current_level_progress_pct,
        streak_days=current_user.streak_days,
        revision_due_count=revision_due_count,
        technologies_progress=tech_progress_items,
        recent_attempts=recent_attempts,
        badges=badges_list,
        weak_topics=weak_topics,
        daily_challenge=daily_challenge
    )

@router.get("/bookmarks", response_model=Dict[str, Any])
async def get_user_bookmarks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    stmt = (
        select(Bookmark)
        .where(Bookmark.user_id == current_user.id)
        .options(
            selectinload(Bookmark.question).selectinload(Question.technology),
            selectinload(Bookmark.question).selectinload(Question.topic)
        )
        .order_by(desc(Bookmark.created_at))
    )
    res = await db.execute(stmt)
    bookmarks = res.scalars().all()

    items = []
    for b in bookmarks:
        q = b.question
        if q:
            items.append({
                "bookmark_id": b.id,
                "question_id": q.id,
                "title": q.title,
                "slug": q.slug,
                "difficulty": q.difficulty,
                "interview_depth": q.interview_depth,
                "question_type": q.question_type,
                "technology_name": q.technology.name if q.technology else "General",
                "technology_slug": q.technology.slug if q.technology else "general",
                "topic_name": q.topic.name if q.topic else None,
                "estimated_time_minutes": q.estimated_time_minutes,
                "created_at": b.created_at
            })

    return {"success": True, "items": items, "total": len(items)}

@router.get("/history", response_model=Dict[str, Any])
async def get_user_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    offset = (page - 1) * limit
    count_stmt = select(func.count(UserAttempt.id)).where(UserAttempt.user_id == current_user.id)
    total = (await db.execute(count_stmt)).scalar_one_or_none() or 0

    stmt = (
        select(UserAttempt)
        .where(UserAttempt.user_id == current_user.id)
        .options(
            selectinload(UserAttempt.question).selectinload(Question.technology),
            selectinload(UserAttempt.question).selectinload(Question.topic)
        )
        .order_by(desc(UserAttempt.created_at))
        .offset(offset)
        .limit(limit)
    )
    res = await db.execute(stmt)
    attempts = res.scalars().all()

    items = []
    for a in attempts:
        q = a.question
        items.append({
            "id": a.id,
            "question_id": a.question_id,
            "question_title": q.title if q else "Question",
            "question_slug": q.slug if q else "",
            "technology_name": q.technology.name if q and q.technology else "General",
            "difficulty": q.difficulty if q else "MEDIUM",
            "candidate_answer": a.candidate_answer,
            "score_overall": a.score_overall,
            "xp_earned": a.xp_earned,
            "time_spent_seconds": a.time_spent_seconds,
            "evaluation_details": a.evaluation_details or {},
            "created_at": a.created_at
        })

    return {
        "success": True,
        "items": items,
        "total": total,
        "page": page,
        "limit": limit
    }

@router.get("/revision", response_model=Dict[str, Any])
async def get_revision_queue(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    srs = SRSService(db)
    cards = await srs.get_due_or_upcoming_cards(current_user.id)
    now = datetime.utcnow()

    items: List[SRSCardRead] = []
    for c in cards:
        q = c.question
        if q:
            items.append(SRSCardRead(
                id=c.id,
                question_id=c.question_id,
                question_title=q.title,
                question_slug=q.slug,
                technology_name=q.technology.name if q.technology else "General",
                difficulty=q.difficulty,
                repetitions=c.repetitions,
                interval_days=c.interval_days,
                ease_factor=c.ease_factor,
                status=c.status,
                next_review_at=c.next_review_at,
                last_reviewed_at=c.last_reviewed_at,
                last_score=c.last_score,
                is_due=c.next_review_at <= now
            ))

    return {
        "success": True,
        "items": items,
        "total": len(items),
        "due_count": sum(1 for i in items if i.is_due)
    }

@router.post("/revision/{question_id}/review", response_model=Dict[str, Any])
async def submit_revision_review(
    question_id: str,
    payload: SRSReviewRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    srs = SRSService(db)
    card = await srs.submit_manual_review(current_user.id, question_id, payload.grade)
    await db.commit()

    return {
        "success": True,
        "message": f"Review recorded with grade {payload.grade}",
        "card": {
            "repetitions": card.repetitions,
            "interval_days": card.interval_days,
            "ease_factor": card.ease_factor,
            "status": card.status,
            "next_review_at": card.next_review_at
        }
    }

@router.get("/badges", response_model=Dict[str, Any])
async def get_user_badges(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    stmt = select(UserBadge).where(UserBadge.user_id == current_user.id)
    earned_badges = {b.badge_key: b for b in (await db.execute(stmt)).scalars().all()}

    badges: List[BadgeRead] = []
    for catalog_badge in BADGE_CATALOG:
        key = catalog_badge["badge_key"]
        earned = earned_badges.get(key)
        badges.append(BadgeRead(
            badge_key=key,
            badge_name=catalog_badge["badge_name"],
            badge_description=catalog_badge["badge_description"],
            icon=catalog_badge["icon"],
            is_unlocked=earned is not None,
            unlocked_at=earned.unlocked_at if earned else None
        ))

    unlocked_count = sum(1 for b in badges if b.is_unlocked)
    return {
        "success": True,
        "badges": badges,
        "unlocked_count": unlocked_count,
        "total_badges": len(badges)
    }

@router.get("/daily-challenge", response_model=Dict[str, Any])
async def get_daily_challenge(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Retrieve question not yet attempted or first available
    stmt_att = select(UserAttempt.question_id).where(UserAttempt.user_id == current_user.id)
    att_qids = set((await db.execute(stmt_att)).scalars().all())

    stmt_q = (
        select(Question)
        .options(selectinload(Question.technology), selectinload(Question.topic))
        .where(Question.id.not_in(att_qids) if att_qids else True)
        .order_by(desc(Question.view_count))
        .limit(1)
    )
    q = (await db.execute(stmt_q)).scalars().first()
    if not q:
        q = (await db.execute(select(Question).options(selectinload(Question.technology)).limit(1))).scalars().first()

    if not q:
        raise HTTPException(status_code=404, detail="No questions available")

    return {
        "success": True,
        "challenge": {
            "id": q.id,
            "title": q.title,
            "slug": q.slug,
            "difficulty": q.difficulty,
            "interview_depth": q.interview_depth,
            "technology_name": q.technology.name if q.technology else "General",
            "topic_name": q.topic.name if q.topic else None,
            "estimated_time_minutes": q.estimated_time_minutes,
            "reward_xp": 100
        }
    }
