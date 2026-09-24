from typing import List, Optional, Tuple, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_, desc, delete
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository
from app.models.question import Question, QuestionHint, QuestionSource, QuestionVersion, QuestionFollowup, QuestionRelation, question_tags
from app.models.taxonomy import Technology, Topic, Tag
from app.models.interaction import Bookmark, UserProgress, UserAttempt, UserNote
from app.schemas.question import QuestionFilterParams

class QuestionRepository(BaseRepository[Question]):
    def __init__(self, session: AsyncSession):
        super().__init__(Question, session)

    async def get_by_id(self, id: str) -> Optional[Question]:
        stmt = (
            select(Question)
            .options(
                selectinload(Question.technology),
                selectinload(Question.topic),
                selectinload(Question.hints),
                selectinload(Question.sources),
                selectinload(Question.tags),
                selectinload(Question.followups),
                selectinload(Question.versions),
            )
            .where(Question.id == id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_slug(self, slug: str) -> Optional[Question]:
        stmt = (
            select(Question)
            .options(
                selectinload(Question.technology),
                selectinload(Question.topic),
                selectinload(Question.hints),
                selectinload(Question.sources),
                selectinload(Question.tags),
                selectinload(Question.followups),
            )
            .where(Question.slug == slug)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_questions(self, params: QuestionFilterParams) -> Tuple[List[Question], int]:
        conditions = [Question.status == "PUBLISHED"]

        if params.technology:
            tech_id = await self.session.scalar(
                select(Technology.id).where(
                    or_(Technology.slug == params.technology, Technology.id == params.technology)
                )
            )
            conditions.append(Question.technology_id == (tech_id or params.technology))

        if params.topic:
            topic_id = await self.session.scalar(
                select(Topic.id).where(
                    or_(Topic.slug == params.topic, Topic.id == params.topic)
                )
            )
            conditions.append(Question.topic_id == (topic_id or params.topic))

        if params.difficulty:
            conditions.append(Question.difficulty == params.difficulty.upper())

        if params.interview_depth:
            conditions.append(Question.interview_depth == params.interview_depth.upper())

        if params.question_type:
            conditions.append(Question.question_type == params.question_type.upper())

        if params.search:
            search_term = f"%{params.search.strip()}%"
            conditions.append(
                or_(
                    Question.title.ilike(search_term),
                    Question.short_answer.ilike(search_term),
                    Question.interview_ready_answer.ilike(search_term)
                )
            )

        count_stmt = select(func.count(Question.id)).where(and_(*conditions))
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar() or 0

        offset = (params.page - 1) * params.limit
        stmt = (
            select(Question)
            .options(
                selectinload(Question.technology),
                selectinload(Question.topic),
                selectinload(Question.tags)
            )
            .where(and_(*conditions))
            .order_by(desc(Question.created_at))
            .offset(offset)
            .limit(params.limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def get_reading_mode_questions(self, technology_slug: str) -> Tuple[Optional[Technology], List[Question]]:
        # 1. Fetch technology
        tech_stmt = select(Technology).where(
            or_(Technology.slug == technology_slug, Technology.id == technology_slug)
        )
        tech_res = await self.session.execute(tech_stmt)
        technology = tech_res.scalars().first()
        if not technology:
            return None, []

        # 2. Fetch all published questions with full content
        conditions = [
            Question.technology_id == technology.id,
            Question.status == "PUBLISHED",
            or_(
                Question.interview_ready_answer.isnot(None),
                Question.short_answer.isnot(None),
                Question.deep_explanation.isnot(None),
            )
        ]

        stmt = (
            select(Question)
            .options(
                selectinload(Question.technology),
                selectinload(Question.topic),
                selectinload(Question.tags),
            )
            .where(and_(*conditions))
        )
        result = await self.session.execute(stmt)
        questions = list(result.scalars().all())
        return technology, questions

    async def increment_view_count(self, question: Question) -> None:
        try:
            from sqlalchemy import update
            await self.session.execute(
                update(Question)
                .where(Question.id == question.id)
                .values(view_count=Question.view_count + 1)
            )
            await self.session.commit()
        except Exception:
            pass

    async def toggle_bookmark(self, user_id: str, question_id: str) -> bool:
        stmt = select(Bookmark).where(Bookmark.user_id == user_id, Bookmark.question_id == question_id)
        result = await self.session.execute(stmt)
        existing = result.scalars().first()
        if existing:
            await self.session.delete(existing)
            await self.session.commit()
            return False
        else:
            new_bookmark = Bookmark(user_id=user_id, question_id=question_id)
            self.session.add(new_bookmark)
            await self.session.commit()
            return True

    async def is_bookmarked(self, user_id: str, question_id: str) -> bool:
        stmt = select(Bookmark).where(Bookmark.user_id == user_id, Bookmark.question_id == question_id)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    async def record_attempt(self, attempt: UserAttempt) -> UserAttempt:
        self.session.add(attempt)
        await self.session.commit()
        await self.session.refresh(attempt)
        return attempt

    async def create_version_snapshot(
        self,
        question_id: str,
        version_number: int,
        change_summary: str,
        snapshot: dict,
        user_id: Optional[str] = None
    ) -> QuestionVersion:
        version = QuestionVersion(
            question_id=question_id,
            version_number=version_number,
            change_summary=change_summary,
            content_snapshot=snapshot,
            created_by=user_id
        )
        self.session.add(version)
        await self.session.commit()
        return version

    async def list_admin_questions(
        self,
        status: Optional[str] = None,
        technology: Optional[str] = None,
        difficulty: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 50
    ) -> Tuple[List[Question], int, Dict[str, int]]:
        conditions = []

        if status and status.upper() != "ALL":
            conditions.append(Question.status == status.upper())

        if technology and technology != "ALL":
            conditions.append(
                or_(
                    Question.technology_id == technology,
                    Question.technology.has(Technology.slug == technology)
                )
            )

        if difficulty and difficulty.upper() != "ALL":
            conditions.append(Question.difficulty == difficulty.upper())

        if search and search.strip():
            search_term = f"%{search.strip()}%"
            conditions.append(
                or_(
                    Question.title.ilike(search_term),
                    Question.slug.ilike(search_term),
                    Question.short_answer.ilike(search_term),
                    Question.interview_ready_answer.ilike(search_term)
                )
            )

        where_clause = and_(*conditions) if conditions else True
        count_stmt = select(func.count(Question.id)).where(where_clause)
        total = (await self.session.execute(count_stmt)).scalar() or 0

        # Status distribution counts
        total_all = (await self.session.execute(select(func.count(Question.id)))).scalar() or 0
        published_count = (await self.session.execute(select(func.count(Question.id)).where(Question.status == "PUBLISHED"))).scalar() or 0
        draft_count = (await self.session.execute(select(func.count(Question.id)).where(Question.status == "DRAFT"))).scalar() or 0
        in_review_count = (await self.session.execute(select(func.count(Question.id)).where(Question.status.in_(["AI_REVIEW", "TECHNICAL_REVIEW", "NEEDS_REVIEW"])))).scalar() or 0
        approved_count = (await self.session.execute(select(func.count(Question.id)).where(Question.status == "APPROVED"))).scalar() or 0
        archived_count = (await self.session.execute(select(func.count(Question.id)).where(Question.status == "ARCHIVED"))).scalar() or 0

        counts = {
            "total": total_all,
            "published": published_count,
            "draft": draft_count,
            "in_review": in_review_count,
            "approved": approved_count,
            "archived": archived_count,
            "filtered": total
        }

        offset = (page - 1) * limit
        stmt = (
            select(Question)
            .options(
                selectinload(Question.technology),
                selectinload(Question.topic),
                selectinload(Question.tags),
                selectinload(Question.hints),
                selectinload(Question.sources),
                selectinload(Question.followups),
            )
            .where(where_clause)
            .order_by(desc(Question.created_at))
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total, counts

    async def delete_question(self, question_id: str) -> bool:
        # Clean up related records
        await self.session.execute(delete(Bookmark).where(Bookmark.question_id == question_id))
        await self.session.execute(delete(UserAttempt).where(UserAttempt.question_id == question_id))
        await self.session.execute(delete(UserNote).where(UserNote.question_id == question_id))
        await self.session.execute(
            delete(QuestionRelation).where(
                or_(
                    QuestionRelation.source_question_id == question_id,
                    QuestionRelation.target_question_id == question_id
                )
            )
        )
        await self.session.execute(delete(question_tags).where(question_tags.c.question_id == question_id))
        await self.session.execute(delete(QuestionHint).where(QuestionHint.question_id == question_id))
        await self.session.execute(delete(QuestionSource).where(QuestionSource.question_id == question_id))
        await self.session.execute(delete(QuestionFollowup).where(QuestionFollowup.question_id == question_id))
        await self.session.execute(delete(QuestionVersion).where(QuestionVersion.question_id == question_id))

        # Delete question
        result = await self.session.execute(delete(Question).where(Question.id == question_id))
        await self.session.commit()
        return result.rowcount > 0

