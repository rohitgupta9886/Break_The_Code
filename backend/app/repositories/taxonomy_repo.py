from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.repositories.base import BaseRepository
from app.models.taxonomy import Domain, Technology, Topic
from app.models.question import Question

class TaxonomyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_technologies(self) -> List[Technology]:
        stmt = select(Technology).where(Technology.is_active == True).order_by(Technology.order_index)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_technologies_with_counts(self) -> List[Tuple[Technology, int]]:
        stmt = (
            select(Technology, func.count(Question.id).label("q_count"))
            .outerjoin(Question, and_(Question.technology_id == Technology.id, Question.status == "PUBLISHED"))
            .where(Technology.is_active == True)
            .group_by(Technology.id)
            .order_by(Technology.order_index)
        )
        result = await self.session.execute(stmt)
        return [(row[0], row[1]) for row in result.all()]

    async def get_technology_by_slug(self, slug: str) -> Optional[Technology]:
        stmt = select(Technology).where(Technology.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_question_count_by_tech(self, tech_id: str) -> int:
        stmt = select(func.count(Question.id)).where(
            Question.technology_id == tech_id,
            Question.status == "PUBLISHED"
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def list_domains_with_technologies(self) -> List[Domain]:
        stmt = select(Domain).order_by(Domain.order_index)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
