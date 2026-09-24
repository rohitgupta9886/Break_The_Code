from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, JSON, Boolean, DateTime, Index
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedBase

class Bookmark(TimeStampedBase):
    __tablename__ = "bookmarks"
    __table_args__ = (
        Index("ix_bookmarks_user_question", "user_id", "question_id", unique=True),
    )

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)

    user = relationship("User", back_populates="bookmarks")
    question = relationship("Question")

class UserProgress(TimeStampedBase):
    __tablename__ = "user_progress"
    __table_args__ = (
        Index("ix_user_progress_user_tech", "user_id", "technology_id", unique=True),
    )

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    technology_id = Column(String(36), ForeignKey("technologies.id", ondelete="CASCADE"), nullable=False, index=True)
    questions_attempted = Column(Integer, default=0, nullable=False)
    questions_completed = Column(Integer, default=0, nullable=False)
    accuracy_rate = Column(Float, default=0.0, nullable=False)

    user = relationship("User", back_populates="progress")
    technology = relationship("Technology")

class UserAttempt(TimeStampedBase):
    __tablename__ = "user_attempts"
    __table_args__ = (
        Index("ix_user_attempts_user_created", "user_id", "created_at"),
    )

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    candidate_answer = Column(Text, nullable=False)
    time_spent_seconds = Column(Integer, default=0, nullable=False)
    score_overall = Column(Float, default=0.0, nullable=False)
    xp_earned = Column(Integer, default=0, nullable=False)
    evaluation_details = Column(JSON, default=dict, nullable=True)

    user = relationship("User", back_populates="attempts")
    question = relationship("Question")

class UserNote(TimeStampedBase):
    __tablename__ = "user_notes"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    note_text = Column(Text, nullable=False)
    is_private = Column(Boolean, default=True, nullable=False)

    user = relationship("User")
    question = relationship("Question")

class SpacedRepetitionCard(TimeStampedBase):
    __tablename__ = "spaced_repetition_cards"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    repetitions = Column(Integer, default=0, nullable=False)
    interval_days = Column(Float, default=1.0, nullable=False)
    ease_factor = Column(Float, default=2.5, nullable=False)
    next_review_at = Column(DateTime, nullable=False, index=True)
    last_reviewed_at = Column(DateTime, nullable=True)
    last_score = Column(Float, nullable=True)
    status = Column(String(20), default="LEARNING", nullable=False)  # LEARNING, REVIEW, MASTERED

    user = relationship("User", back_populates="revision_cards")
    question = relationship("Question")

class UserBadge(TimeStampedBase):
    __tablename__ = "user_badges"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    badge_key = Column(String(50), nullable=False, index=True)
    badge_name = Column(String(100), nullable=False)
    badge_description = Column(String(255), nullable=False)
    icon = Column(String(50), default="Trophy", nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="badges")

