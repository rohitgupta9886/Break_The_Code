import re
import time
from datetime import datetime, timezone
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.question_repo import QuestionRepository
from app.repositories.taxonomy_repo import TaxonomyRepository
from app.models.question import Question, QuestionHint, QuestionSource, QuestionFollowup
from app.models.taxonomy import Tag
from app.schemas.question import (
    QuestionFilterParams,
    QuestionCreateSchema,
    QuestionUpdateSchema,
    QuestionCardSchema,
    QuestionDetailSchema
)

# In-memory TTL cache for reading mode data: {slug: (data, timestamp)}
_READING_MODE_CACHE: Dict[str, Tuple[Dict[str, Any], float]] = {}
_CACHE_TTL_SECONDS = 600.0

def invalidate_reading_mode_cache(technology_slug: Optional[str] = None):
    if technology_slug:
        _READING_MODE_CACHE.pop(technology_slug, None)
    else:
        _READING_MODE_CACHE.clear()

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return re.sub(r'^-+|-+$', '', text)

class QuestionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.question_repo = QuestionRepository(session)
        self.taxonomy_repo = TaxonomyRepository(session)

    async def get_by_slug(self, slug: str, increment_view: bool = True) -> Question:
        question = await self.question_repo.get_by_slug(slug)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with slug '{slug}' not found"
            )
        if increment_view:
            await self.question_repo.increment_view_count(question)
        return question

    async def list_questions(self, params: QuestionFilterParams) -> Tuple[List[dict], int]:
        questions, total = await self.question_repo.list_questions(params)
        
        cards = []
        for q in questions:
            cards.append({
                "id": q.id,
                "slug": q.slug,
                "title": q.title,
                "difficulty": q.difficulty,
                "interview_depth": q.interview_depth,
                "question_type": q.question_type,
                "estimated_time_minutes": q.estimated_time_minutes,
                "role_target": q.role_target,
                "interview_round": q.interview_round,
                "technology_name": q.technology.name if q.technology else None,
                "technology_slug": q.technology.slug if q.technology else None,
                "topic_name": q.topic.name if q.topic else None,
                "view_count": q.view_count,
                "upvote_count": q.upvote_count,
                "status": q.status,
                "tags": [{"name": t.name, "slug": t.slug} for t in q.tags] if q.tags else [],
                "created_at": q.created_at
            })
        return cards, total

    async def create_question(self, q_in: QuestionCreateSchema, user_id: Optional[str] = None) -> Question:
        slug = q_in.slug or slugify(q_in.title)
        existing = await self.question_repo.get_by_slug(slug)
        if existing:
            slug = f"{slug}-{q_in.difficulty.lower()}"

        question = Question(
            slug=slug,
            title=q_in.title,
            technology_id=q_in.technology_id,
            topic_id=q_in.topic_id,
            difficulty=q_in.difficulty.upper(),
            interview_depth=q_in.interview_depth.upper(),
            question_type=q_in.question_type.upper(),
            role_target=q_in.role_target,
            experience_level=q_in.experience_level,
            estimated_time_minutes=q_in.estimated_time_minutes,
            short_answer=q_in.short_answer,
            interview_ready_answer=q_in.interview_ready_answer,
            deep_explanation=q_in.deep_explanation,
            architecture_notes=q_in.architecture_notes,
            code_example=q_in.code_example,
            common_mistakes=q_in.common_mistakes or [],
            interviewer_intent=q_in.interviewer_intent,
            status=q_in.status.upper(),
            content_origin=q_in.content_origin.upper(),
            created_by=user_id
        )

        # Attach Hints
        if q_in.hints:
            for h in q_in.hints:
                question.hints.append(
                    QuestionHint(
                        hint_level=h.get("hint_level", 1),
                        hint_type=h.get("hint_type", "CONCEPTUAL"),
                        content=h.get("content", "")
                    )
                )

        # Attach Sources
        if q_in.sources:
            for s in q_in.sources:
                question.sources.append(
                    QuestionSource(
                        source_name=s.get("source_name", "Documentation"),
                        source_url=s.get("source_url"),
                        license=s.get("license", "Attribution"),
                        attribution_required=s.get("attribution_required", 1)
                    )
                )

        # Attach Followups
        if q_in.followups:
            for f in q_in.followups:
                question.followups.append(
                    QuestionFollowup(
                        followup_question=f.get("followup_question", ""),
                        answer_guidance=f.get("answer_guidance")
                    )
                )

        created = await self.question_repo.create(question)
        
        # Save initial version snapshot
        await self.question_repo.create_version_snapshot(
            question_id=created.id,
            version_number=1,
            change_summary="Initial creation",
            snapshot={"title": created.title, "status": created.status},
            user_id=user_id
        )
        return created

    async def toggle_bookmark(self, user_id: str, question_id: str) -> bool:
        return await self.question_repo.toggle_bookmark(user_id, question_id)

    async def get_by_id(self, question_id: str) -> Question:
        question = await self.question_repo.get_by_id(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID '{question_id}' not found"
            )
        return question

    async def list_admin_questions(
        self,
        status: Optional[str] = None,
        technology: Optional[str] = None,
        difficulty: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 50
    ) -> Tuple[List[dict], int, Dict[str, int]]:
        questions, total, counts = await self.question_repo.list_admin_questions(
            status=status,
            technology=technology,
            difficulty=difficulty,
            search=search,
            page=page,
            limit=limit
        )
        
        cards = []
        for q in questions:
            cards.append({
                "id": q.id,
                "slug": q.slug,
                "title": q.title,
                "difficulty": q.difficulty,
                "difficulty_score": getattr(q, "difficulty_score", 5.0),
                "interview_depth": q.interview_depth,
                "question_type": q.question_type,
                "scenario_type": getattr(q, "scenario_type", None),
                "estimated_time_minutes": q.estimated_time_minutes,
                "role_target": q.role_target,
                "experience_level": q.experience_level,
                "interview_round": q.interview_round,
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
                "technology_name": q.technology.name if q.technology else None,
                "technology_slug": q.technology.slug if q.technology else None,
                "technology_id": q.technology_id,
                "topic_name": q.topic.name if q.topic else None,
                "topic_id": q.topic_id,
                "view_count": q.view_count,
                "upvote_count": q.upvote_count,
                "status": q.status,
                "content_origin": q.content_origin,
                "overall_quality_score": getattr(q, "overall_quality_score", 0.94),
                "hints": [{"hint_level": h.hint_level, "hint_type": h.hint_type, "content": h.content} for h in q.hints] if q.hints else [],
                "sources": [{"source_name": s.source_name, "source_url": s.source_url, "license": s.license} for s in q.sources] if q.sources else [],
                "followups": [{"followup_question": f.followup_question, "answer_guidance": f.answer_guidance} for f in q.followups] if q.followups else [],
                "tags": [{"name": t.name, "slug": t.slug} for t in q.tags] if q.tags else [],
                "created_at": q.created_at.isoformat() if q.created_at else None,
                "last_reviewed_at": q.last_reviewed_at.isoformat() if q.last_reviewed_at else None,
            })
        return cards, total, counts

    async def update_question(
        self,
        question_id: str,
        q_update: QuestionUpdateSchema,
        user_id: Optional[str] = None
    ) -> Question:
        question = await self.get_by_id(question_id)

        update_dict = q_update.model_dump(exclude_unset=True)

        scalar_fields = [
            "title", "slug", "technology_id", "topic_id", "difficulty",
            "interview_depth", "question_type", "role_target", "experience_level",
            "interview_round", "estimated_time_minutes", "short_answer",
            "interview_ready_answer", "deep_explanation", "architecture_notes",
            "code_example", "why_interviewer_asks", "interviewer_intent",
            "production_considerations", "failure_modes", "tradeoffs",
            "common_mistakes", "status", "content_origin"
        ]

        for field in scalar_fields:
            if field in update_dict and update_dict[field] is not None:
                val = update_dict[field]
                if field in ["difficulty", "interview_depth", "question_type", "status", "content_origin"] and isinstance(val, str):
                    val = val.upper()
                setattr(question, field, val)

        if "hints" in update_dict and update_dict["hints"] is not None:
            question.hints.clear()
            for h in update_dict["hints"]:
                question.hints.append(
                    QuestionHint(
                        hint_level=h.get("hint_level", 1),
                        hint_type=h.get("hint_type", "CONCEPTUAL"),
                        content=h.get("content", "")
                    )
                )

        if "sources" in update_dict and update_dict["sources"] is not None:
            question.sources.clear()
            for s in update_dict["sources"]:
                question.sources.append(
                    QuestionSource(
                        source_name=s.get("source_name", "Documentation"),
                        source_url=s.get("source_url"),
                        license=s.get("license", "Attribution"),
                        attribution_required=s.get("attribution_required", 1)
                    )
                )

        if "followups" in update_dict and update_dict["followups"] is not None:
            question.followups.clear()
            for f in update_dict["followups"]:
                question.followups.append(
                    QuestionFollowup(
                        followup_question=f.get("followup_question", ""),
                        answer_guidance=f.get("answer_guidance")
                    )
                )

        question.last_reviewed_at = datetime.now(timezone.utc)
        await self.question_repo.update(question)

        version_num = (len(question.versions) if question.versions else 0) + 1
        await self.question_repo.create_version_snapshot(
            question_id=question.id,
            version_number=version_num,
            change_summary=f"Question updated by admin ({user_id or 'admin'})",
            snapshot={"title": question.title, "status": question.status},
            user_id=user_id
        )

        invalidate_reading_mode_cache()
        return question

    async def update_question_status(
        self,
        question_id: str,
        new_status: str,
        note: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Question:
        question = await self.get_by_id(question_id)
        old_status = question.status
        question.status = new_status.upper()
        question.last_reviewed_at = datetime.now(timezone.utc)
        await self.question_repo.update(question)

        version_num = (len(question.versions) if question.versions else 0) + 1
        await self.question_repo.create_version_snapshot(
            question_id=question.id,
            version_number=version_num,
            change_summary=f"Status transitioned from {old_status} to {question.status}. Note: {note or 'None'}",
            snapshot={"status": question.status, "note": note},
            user_id=user_id
        )

        invalidate_reading_mode_cache()
        return question

    async def delete_question(self, question_id: str, user_id: Optional[str] = None) -> bool:
        question = await self.get_by_id(question_id)
        tech_slug = question.technology.slug if question.technology else None
        success = await self.question_repo.delete_question(question_id)
        if success:
            invalidate_reading_mode_cache(tech_slug)
        return success

    async def publish_question(self, question_id: str, user_id: Optional[str] = None) -> Question:
        return await self.update_question_status(question_id, "PUBLISHED", "Published to public portal", user_id=user_id)


    async def get_reading_mode_data(self, technology_slug: str, current_user_id: Optional[str] = None) -> Dict[str, Any]:
        now = time.time()
        cached = _READING_MODE_CACHE.get(technology_slug)
        if cached:
            cached_data, cached_time = cached
            if now - cached_time < _CACHE_TTL_SECONDS:
                return cached_data

        technology, questions = await self.question_repo.get_reading_mode_questions(technology_slug)
        if not technology:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Technology with slug '{technology_slug}' not found"
            )

        # 8 Difficulty Tiers metadata & ordering
        TIER_ORDER = [
            "BASIC",
            "MEDIUM",
            "HARD",
            "TOUGH",
            "VERY_TOUGH",
            "VERY_VERY_TOUGH",
            "PRODUCTION_SCENARIO",
            "EXPERT_DEEP_DIVE",
        ]

        TIER_METADATA = {
            "BASIC": {
                "tier": "BASIC",
                "level_code": "L1",
                "label": "Basic",
                "sub": "Fundamentals",
                "experience_range": "Freshers / 0–2 Years Experience",
                "description": "Fundamental mechanics, core runtime concepts, and baseline architecture questions.",
                "badge_color": "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border-emerald-500/30",
            },
            "MEDIUM": {
                "tier": "MEDIUM",
                "level_code": "L2",
                "label": "Medium",
                "sub": "Foundations & Memory",
                "experience_range": "3–5 Years Experience",
                "description": "Internal implementation details, memory management, and practical algorithmic patterns.",
                "badge_color": "bg-sky-500/15 text-sky-700 dark:text-sky-300 border-sky-500/30",
            },
            "HARD": {
                "tier": "HARD",
                "level_code": "L3",
                "label": "Hard",
                "sub": "Concurrency & State",
                "experience_range": "5+ Years / Senior Engineer",
                "description": "Complex concurrency, state graph cycles, lock-free structures, and architectural trade-offs.",
                "badge_color": "bg-indigo-500/15 text-indigo-700 dark:text-indigo-300 border-indigo-500/30",
            },
            "TOUGH": {
                "tier": "TOUGH",
                "level_code": "L4",
                "label": "Tough",
                "sub": "Systems & Bottlenecks",
                "experience_range": "Staff / Lead Engineer",
                "description": "Performance bottlenecks, query execution plans, and zero-copy pipelines.",
                "badge_color": "bg-amber-500/15 text-amber-800 dark:text-amber-300 border-amber-500/30",
            },
            "VERY_TOUGH": {
                "tier": "VERY_TOUGH",
                "level_code": "L5",
                "label": "Very Tough",
                "sub": "Scale & Split-Brain",
                "experience_range": "Principal Engineer",
                "description": "Distributed partitions, consensus protocols, and fault injection resiliency.",
                "badge_color": "bg-orange-500/15 text-orange-700 dark:text-orange-300 border-orange-500/30",
            },
            "VERY_VERY_TOUGH": {
                "tier": "VERY_VERY_TOUGH",
                "level_code": "L6",
                "label": "Very Very Tough",
                "sub": "Consensus & Raft",
                "experience_range": "Principal / Domain Specialist",
                "description": "Formal state machine replication, linearizability, and low-level protocol designs.",
                "badge_color": "bg-rose-500/15 text-rose-700 dark:text-rose-300 border-rose-500/30",
            },
            "PRODUCTION_SCENARIO": {
                "tier": "PRODUCTION_SCENARIO",
                "level_code": "L7",
                "label": "Production Scenario",
                "sub": "Live Incidents & Outages",
                "experience_range": "Staff SRE / Production Architect",
                "description": "Real-world SEV-1 outage mitigation, cascading connection pool exhaustions, and zero-downtime migrations.",
                "badge_color": "bg-teal-500/15 text-teal-700 dark:text-teal-300 border-teal-500/30",
            },
            "EXPERT_DEEP_DIVE": {
                "tier": "EXPERT_DEEP_DIVE",
                "level_code": "L8",
                "label": "Expert Deep Dive",
                "sub": "Principal & Distinguished Architect",
                "experience_range": "Distinguished Engineer / Architect",
                "description": "Bytecode manipulation, custom kernel memory bypass, distributed graph compilers, and hardware-level limits.",
                "badge_color": "bg-purple-500/15 text-purple-700 dark:text-purple-300 border-purple-500/30",
            },
        }

        # Group questions by tier
        grouped: Dict[str, List[Dict[str, Any]]] = {t: [] for t in TIER_ORDER}
        counts_by_tier: Dict[str, int] = {t: 0 for t in TIER_ORDER}

        for q in questions:
            tier_key = q.difficulty if q.difficulty in TIER_METADATA else "MEDIUM"
            counts_by_tier[tier_key] = counts_by_tier.get(tier_key, 0) + 1

            q_data = {
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
                "view_count": q.view_count,
                "upvote_count": q.upvote_count,
                "created_at": q.created_at.isoformat() if hasattr(q.created_at, "isoformat") else str(q.created_at),
                "topic_name": q.topic.name if q.topic else None,
                "topic_slug": q.topic.slug if q.topic else None,
                "hints": [],
                "sources": [],
                "followups": [],
                "tags": [{"name": t.name, "slug": t.slug} for t in q.tags],
            }
            grouped[tier_key].append(q_data)

        # Build non-empty tiers
        tiers_output = []
        for tier_key in TIER_ORDER:
            tier_questions = grouped[tier_key]
            if not tier_questions:
                continue

            # Deterministic ordering within tier: by topic, difficulty score, and question creation sequence
            tier_questions.sort(key=lambda x: (
                x.get("topic_name") or "",
                x.get("difficulty_score") if x.get("difficulty_score") is not None else 5.0,
                x.get("created_at") or "",
                x.get("title") or ""
            ))

            meta = TIER_METADATA[tier_key]
            tiers_output.append({
                **meta,
                "count": len(tier_questions),
                "questions": tier_questions,
            })

        topics_data = []
        if hasattr(technology, "topics") and technology.topics:
            topics_data = [{"id": top.id, "name": top.name, "slug": top.slug} for top in technology.topics]

        result_data = {
            "success": True,
            "technology": {
                "id": technology.id,
                "name": technology.name,
                "slug": technology.slug,
                "short_description": getattr(technology, "short_description", ""),
                "icon": getattr(technology, "icon", "Layers"),
                "question_count": len(questions),
                "topics": topics_data,
                "technology_version": "Current (2026)",
                "last_reviewed_at": datetime.now(timezone.utc).isoformat(),
            },
            "summary": {
                "total_questions": len(questions),
                "total_tiers": len(tiers_output),
                "counts_by_tier": counts_by_tier,
            },
            "tiers": tiers_output,
        }

        _READING_MODE_CACHE[technology_slug] = (result_data, now)
        return result_data
