from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.interaction import SpacedRepetitionCard
from app.models.question import Question

class SRSService:
    """
    SuperMemo SM-2 Spaced Repetition Algorithm Implementation.
    Calculates dynamic review intervals and ease factors based on candidate recall scores.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def score_to_grade(score: float) -> int:
        if score >= 9.0:
            return 5
        elif score >= 8.0:
            return 4
        elif score >= 7.0:
            return 3
        elif score >= 5.0:
            return 2
        elif score >= 3.0:
            return 1
        return 0

    @staticmethod
    def calculate_sm2(repetitions: int, interval_days: float, ease_factor: float, grade: int) -> Tuple[int, float, float, str]:
        if grade < 3:
            new_repetitions = 0
            new_interval = 1.0
            new_ease = max(1.3, ease_factor - 0.2)
            new_status = "LEARNING"
        else:
            if repetitions == 0:
                new_interval = 1.0
            elif repetitions == 1:
                new_interval = 6.0
            else:
                new_interval = round(interval_days * ease_factor, 1)

            # SM-2 ease factor formula: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
            new_ease = max(1.3, ease_factor + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02)))
            new_repetitions = repetitions + 1
            new_status = "MASTERED" if (new_repetitions >= 4 and new_ease >= 2.3) else "REVIEW"

        return new_repetitions, new_interval, round(new_ease, 2), new_status

    async def get_card(self, user_id: str, question_id: str) -> Optional[SpacedRepetitionCard]:
        stmt = select(SpacedRepetitionCard).where(
            SpacedRepetitionCard.user_id == user_id,
            SpacedRepetitionCard.question_id == question_id
        )
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def process_attempt(self, user_id: str, question_id: str, score: float) -> SpacedRepetitionCard:
        grade = self.score_to_grade(score)
        card = await self.get_card(user_id, question_id)

        now = datetime.utcnow()
        if not card:
            reps, interval, ease, status = self.calculate_sm2(0, 1.0, 2.5, grade)
            card = SpacedRepetitionCard(
                user_id=user_id,
                question_id=question_id,
                repetitions=reps,
                interval_days=interval,
                ease_factor=ease,
                status=status,
                next_review_at=now + timedelta(days=interval),
                last_reviewed_at=now,
                last_score=score
            )
            self.session.add(card)
        else:
            reps, interval, ease, status = self.calculate_sm2(card.repetitions, card.interval_days, card.ease_factor, grade)
            card.repetitions = reps
            card.interval_days = interval
            card.ease_factor = ease
            card.status = status
            card.last_reviewed_at = now
            card.last_score = score
            card.next_review_at = now + timedelta(days=interval)

        return card

    async def submit_manual_review(self, user_id: str, question_id: str, grade: int) -> SpacedRepetitionCard:
        grade = max(1, min(5, grade))
        card = await self.get_card(user_id, question_id)
        now = datetime.utcnow()

        if not card:
            reps, interval, ease, status = self.calculate_sm2(0, 1.0, 2.5, grade)
            card = SpacedRepetitionCard(
                user_id=user_id,
                question_id=question_id,
                repetitions=reps,
                interval_days=interval,
                ease_factor=ease,
                status=status,
                next_review_at=now + timedelta(days=interval),
                last_reviewed_at=now,
                last_score=float(grade * 2.0)
            )
            self.session.add(card)
        else:
            reps, interval, ease, status = self.calculate_sm2(card.repetitions, card.interval_days, card.ease_factor, grade)
            card.repetitions = reps
            card.interval_days = interval
            card.ease_factor = ease
            card.status = status
            card.last_reviewed_at = now
            card.last_score = float(grade * 2.0)
            card.next_review_at = now + timedelta(days=interval)

        return card

    async def get_due_or_upcoming_cards(self, user_id: str, limit: int = 30) -> List[SpacedRepetitionCard]:
        stmt = (
            select(SpacedRepetitionCard)
            .where(SpacedRepetitionCard.user_id == user_id)
            .options(
                selectinload(SpacedRepetitionCard.question).selectinload(Question.technology),
                selectinload(SpacedRepetitionCard.question).selectinload(Question.topic)
            )
            .order_by(SpacedRepetitionCard.next_review_at.asc())
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
