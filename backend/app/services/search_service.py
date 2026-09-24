from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc
from app.models.question import Question
from app.models.taxonomy import Technology, Topic

class SearchService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def hybrid_search(self, query: str, limit: int = 15) -> List[Dict[str, Any]]:
        query_clean = query.strip()
        if not query_clean:
            return []

        search_pattern = f"%{query_clean}%"
        stmt = (
            select(Question)
            .where(
                Question.status == "PUBLISHED",
                or_(
                    Question.title.ilike(search_pattern),
                    Question.short_answer.ilike(search_pattern),
                    Question.interview_ready_answer.ilike(search_pattern),
                    Question.deep_explanation.ilike(search_pattern),
                )
            )
            .order_by(desc(Question.upvote_count), desc(Question.view_count))
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        questions = result.scalars().all()

        results = []
        for q in questions:
            results.append({
                "id": q.id,
                "slug": q.slug,
                "title": q.title,
                "difficulty": q.difficulty,
                "interview_depth": q.interview_depth,
                "question_type": q.question_type,
                "technology_name": q.technology.name if q.technology else None,
                "technology_slug": q.technology.slug if q.technology else None,
                "topic_name": q.topic.name if q.topic else None,
                "match_snippet": q.short_answer or q.title
            })
        return results

    async def autocomplete(self, query: str, limit: int = 8) -> Dict[str, List[Dict[str, str]]]:
        pattern = f"%{query.strip()}%"
        
        # Questions
        q_stmt = select(Question.title, Question.slug).where(Question.status == "PUBLISHED", Question.title.ilike(pattern)).limit(limit)
        q_res = await self.session.execute(q_stmt)
        question_matches = [{"title": row[0], "slug": row[1]} for row in q_res.all()]

        # Technologies
        t_stmt = select(Technology.name, Technology.slug).where(Technology.is_active == True, Technology.name.ilike(pattern)).limit(limit)
        t_res = await self.session.execute(t_stmt)
        tech_matches = [{"name": row[0], "slug": row[1]} for row in t_res.all()]

        # Topics
        top_stmt = select(Topic.name, Topic.slug).where(Topic.name.ilike(pattern)).limit(limit)
        top_res = await self.session.execute(top_stmt)
        topic_matches = [{"name": row[0], "slug": row[1]} for row in top_res.all()]

        return {
            "questions": question_matches,
            "technologies": tech_matches,
            "topics": topic_matches
        }
