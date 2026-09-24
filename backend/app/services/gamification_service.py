from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user import User
from app.models.question import Question
from app.models.interaction import UserAttempt, UserProgress, UserBadge

BADGE_CATALOG = [
    {
        "badge_key": "FIRST_STEP",
        "badge_name": "First Step Taken",
        "badge_description": "Completed your first technical interview problem.",
        "icon": "Zap",
    },
    {
        "badge_key": "HIGH_ROLLER",
        "badge_name": "Elite Performer",
        "badge_description": "Achieved a 9.0+ score on an interview problem.",
        "icon": "Award",
    },
    {
        "badge_key": "DEEP_THINKER",
        "badge_name": "Deep Thinker",
        "badge_description": "Successfully tackled an L4/L5 deep dive architecture problem.",
        "icon": "Cpu",
    },
    {
        "badge_key": "AI_PIONEER",
        "badge_name": "Agentic Pioneer",
        "badge_description": "Solved 3+ LangGraph, RAG, or AI architecture questions.",
        "icon": "Bot",
    },
    {
        "badge_key": "JVM_MAESTRO",
        "badge_name": "JVM Maestro",
        "badge_description": "Conquered 3+ Java concurrency, GC, or Spring Boot questions.",
        "icon": "Coffee",
    },
    {
        "badge_key": "DSA_GLADIATOR",
        "badge_name": "Algorithmic Gladiator",
        "badge_description": "Solved 3+ complex dynamic programming or graph problems.",
        "icon": "Binary",
    },
    {
        "badge_key": "STREAK_3",
        "badge_name": "Consistency Champion",
        "badge_description": "Maintained an active practice streak of 3+ consecutive days.",
        "icon": "Flame",
    },
    {
        "badge_key": "TEN_CLUB",
        "badge_name": "Tenacious 10",
        "badge_description": "Completed 10 comprehensive interview evaluations.",
        "icon": "ShieldCheck",
    },
]

class GamificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def calculate_xp(self, score: float, time_spent_seconds: int) -> int:
        base_xp = 50
        
        # Performance bonus
        if score >= 9.0:
            score_bonus = 40
        elif score >= 8.0:
            score_bonus = 25
        elif score >= 7.0:
            score_bonus = 15
        elif score >= 5.0:
            score_bonus = 5
        else:
            score_bonus = 0

        # Time deliberation bonus (thoughtful effort)
        time_bonus = 10 if time_spent_seconds >= 60 else (5 if time_spent_seconds >= 30 else 0)
        
        return base_xp + score_bonus + time_bonus

    def update_streak(self, user: User) -> int:
        now = datetime.utcnow()
        today = now.date()

        if not user.last_active_date:
            user.streak_days = 1
        else:
            last_date = user.last_active_date.date()
            diff_days = (today - last_date).days
            if diff_days == 1:
                user.streak_days += 1
            elif diff_days == 0:
                # Already logged activity today, preserve streak
                pass
            else:
                user.streak_days = 1

        user.last_active_date = now
        return user.streak_days

    async def update_user_progress(self, user_id: str, technology_id: Optional[str], score: float):
        if not technology_id:
            return

        stmt = select(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.technology_id == technology_id
        )
        res = await self.session.execute(stmt)
        progress = res.scalars().first()

        if not progress:
            progress = UserProgress(
                user_id=user_id,
                technology_id=technology_id,
                questions_attempted=1,
                questions_completed=1 if score >= 7.0 else 0,
                accuracy_rate=score * 10.0
            )
            self.session.add(progress)
        else:
            prev_attempts = progress.questions_attempted
            progress.questions_attempted += 1
            if score >= 7.0:
                progress.questions_completed += 1
            # Rolling average accuracy
            new_acc = ((progress.accuracy_rate * prev_attempts) + (score * 10.0)) / progress.questions_attempted
            progress.accuracy_rate = round(new_acc, 1)

    async def check_and_award_badges(
        self,
        user: User,
        current_attempt: UserAttempt,
        question: Optional[Question]
    ) -> List[UserBadge]:
        # Fetch existing badges for user
        badge_stmt = select(UserBadge.badge_key).where(UserBadge.user_id == user.id)
        res = await self.session.execute(badge_stmt)
        earned_keys = set(res.scalars().all())

        newly_earned: List[UserBadge] = []

        # Count total attempts
        count_stmt = select(func.count(UserAttempt.id)).where(UserAttempt.user_id == user.id)
        total_attempts = (await self.session.execute(count_stmt)).scalar_one_or_none() or 0

        # Check badge rules
        eligible_keys = []

        # 1. FIRST_STEP
        if total_attempts >= 1 and "FIRST_STEP" not in earned_keys:
            eligible_keys.append("FIRST_STEP")

        # 2. HIGH_ROLLER
        if current_attempt.score_overall >= 9.0 and "HIGH_ROLLER" not in earned_keys:
            eligible_keys.append("HIGH_ROLLER")

        # 3. DEEP_THINKER
        if question and question.interview_depth == "DEEP_DIVE" and current_attempt.score_overall >= 7.0:
            if "DEEP_THINKER" not in earned_keys:
                eligible_keys.append("DEEP_THINKER")

        # 4. STREAK_3
        if user.streak_days >= 3 and "STREAK_3" not in earned_keys:
            eligible_keys.append("STREAK_3")

        # 5. TEN_CLUB
        if total_attempts >= 10 and "TEN_CLUB" not in earned_keys:
            eligible_keys.append("TEN_CLUB")

        # Technology specific badge queries
        if question and question.technology:
            tech_slug = question.technology.slug
            if "langgraph" in tech_slug or "rag" in tech_slug or "ai" in tech_slug:
                if "AI_PIONEER" not in earned_keys:
                    tech_attempts_stmt = select(func.count(UserAttempt.id)).join(
                        Question, Question.id == UserAttempt.question_id
                    ).where(
                        UserAttempt.user_id == user.id,
                        Question.technology_id == question.technology_id
                    )
                    ai_cnt = (await self.session.execute(tech_attempts_stmt)).scalar_one_or_none() or 0
                    if ai_cnt >= 3:
                        eligible_keys.append("AI_PIONEER")

            if "java" in tech_slug and "JVM_MAESTRO" not in earned_keys:
                tech_attempts_stmt = select(func.count(UserAttempt.id)).join(
                    Question, Question.id == UserAttempt.question_id
                ).where(
                    UserAttempt.user_id == user.id,
                    Question.technology_id == question.technology_id
                )
                java_cnt = (await self.session.execute(tech_attempts_stmt)).scalar_one_or_none() or 0
                if java_cnt >= 3:
                    eligible_keys.append("JVM_MAESTRO")

            if "dsa" in tech_slug and "DSA_GLADIATOR" not in earned_keys:
                tech_attempts_stmt = select(func.count(UserAttempt.id)).join(
                    Question, Question.id == UserAttempt.question_id
                ).where(
                    UserAttempt.user_id == user.id,
                    Question.technology_id == question.technology_id
                )
                dsa_cnt = (await self.session.execute(tech_attempts_stmt)).scalar_one_or_none() or 0
                if dsa_cnt >= 3:
                    eligible_keys.append("DSA_GLADIATOR")

        # Instantiate and save newly earned badges
        catalog_map = {b["badge_key"]: b for b in BADGE_CATALOG}
        for key in eligible_keys:
            meta = catalog_map.get(key)
            if meta:
                badge = UserBadge(
                    user_id=user.id,
                    badge_key=key,
                    badge_name=meta["badge_name"],
                    badge_description=meta["badge_description"],
                    icon=meta["icon"],
                    unlocked_at=datetime.utcnow()
                )
                self.session.add(badge)
                newly_earned.append(badge)

        return newly_earned
