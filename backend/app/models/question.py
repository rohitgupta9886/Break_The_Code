from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, JSON, DateTime, Table, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.base import TimeStampedBase, generate_uuid
from app.core.database import Base

question_tags = Table(
    "question_tags",
    Base.metadata,
    Column("question_id", String(36), ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", String(36), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

class Question(TimeStampedBase):
    __tablename__ = "questions"
    __table_args__ = (
        Index("ix_questions_tech_status", "technology_id", "status"),
        Index("ix_questions_diff_status", "difficulty", "status"),
        Index("ix_questions_tech_diff_status", "technology_id", "difficulty", "status"),
        Index("ix_questions_created_at_desc", "created_at"),
    )

    slug = Column(String(255), unique=True, index=True, nullable=False)
    technology_id = Column(String(36), ForeignKey("technologies.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="SET NULL"), nullable=True, index=True)

    title = Column(String(500), nullable=False)
    
    # 8 Public Difficulty Levels:
    # BASIC, MEDIUM, HARD, TOUGH, VERY_TOUGH, VERY_VERY_TOUGH, PRODUCTION_SCENARIO, EXPERT_DEEP_DIVE
    difficulty = Column(String(30), default="MEDIUM", nullable=False, index=True)
    difficulty_score = Column(Float, default=5.0, nullable=False) # 1.0 (Basic) to 10.0 (Expert)
    
    interview_depth = Column(String(10), default="L2", nullable=False) # L1, L2, L3, L4, L5
    question_type = Column(String(50), default="CONCEPTUAL", nullable=False, index=True)
    scenario_type = Column(String(100), nullable=True) # e.g., DISTRIBUTED_CRASH, CONCURRENCY_SPIKE, LATENCY_BUDGET
    
    role_target = Column(String(100), default="Software Engineer", nullable=True)
    experience_level = Column(String(50), default="All Levels", nullable=True)
    interview_round = Column(String(50), default="Technical Screen", nullable=True)
    estimated_time_minutes = Column(Integer, default=5, nullable=False)

    # 15-Part Answer DNA Components
    short_answer = Column(Text, nullable=True) # 1. Direct Answer
    interview_ready_answer = Column(Text, nullable=False) # 2. Interview-Ready Answer
    deep_explanation = Column(Text, nullable=True) # 3. Core Concept & 4. Detailed Explanation
    architecture_notes = Column(Text, nullable=True) # 7. Architecture / Flow Notes
    code_example = Column(Text, nullable=True) # 6. Practical Code Implementation
    
    why_interviewer_asks = Column(Text, nullable=True) # 8. Why Interviewer Asks This
    interviewer_intent = Column(Text, nullable=True) # Intent Enum / Reasoning
    
    production_considerations = Column(Text, nullable=True) # 9. Production Considerations
    failure_modes = Column(Text, nullable=True) # 10. Failure Modes
    tradeoffs = Column(Text, nullable=True) # 11. Trade-offs
    common_mistakes = Column(JSON, default=list, nullable=True) # 12. Common Mistakes

    # Lifecycle & Review Engine
    # DRAFT, GENERATED, TECHNICAL_REVIEW, NEEDS_REVIEW, APPROVED, PUBLISHED, OUTDATED, ARCHIVED
    status = Column(String(30), default="PUBLISHED", nullable=False, index=True)
    content_origin = Column(String(30), default="ORIGINAL", nullable=False) # ORIGINAL, ADAPTED, SYNTHESIZED

    # Internal Quality Scores (0.0 to 1.0)
    technical_accuracy_score = Column(Float, default=0.95, nullable=False)
    answer_quality_score = Column(Float, default=0.92, nullable=False)
    difficulty_accuracy_score = Column(Float, default=0.90, nullable=False)
    originality_score = Column(Float, default=0.98, nullable=False)
    production_relevance_score = Column(Float, default=0.94, nullable=False)
    source_quality_score = Column(Float, default=0.95, nullable=False)
    overall_quality_score = Column(Float, default=0.94, nullable=False)

    # Version-Awareness
    technology_version = Column(String(50), default="Current (2026)", nullable=True)
    last_reviewed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    review_due_at = Column(DateTime(timezone=True), nullable=True)

    view_count = Column(Integer, default=0, nullable=False)
    upvote_count = Column(Integer, default=0, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    technology = relationship("Technology", back_populates="questions", lazy="selectin")
    topic = relationship("Topic", back_populates="questions", lazy="selectin")
    tags = relationship("Tag", secondary=question_tags, lazy="selectin")
    hints = relationship("QuestionHint", back_populates="question", cascade="all, delete-orphan", lazy="selectin")
    sources = relationship("QuestionSource", back_populates="question", cascade="all, delete-orphan", lazy="selectin")
    versions = relationship("QuestionVersion", back_populates="question", cascade="all, delete-orphan")
    followups = relationship("QuestionFollowup", back_populates="question", cascade="all, delete-orphan", lazy="selectin")
    outgoing_relations = relationship(
        "QuestionRelation", 
        foreign_keys="[QuestionRelation.source_question_id]", 
        cascade="all, delete-orphan",
        lazy="selectin"
    )

class QuestionRelation(TimeStampedBase):
    __tablename__ = "question_relations"

    source_question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    target_question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    relation_type = Column(String(50), nullable=False, index=True) 
    # PREREQUISITE, RELATED, HARDER_VERSION, EASIER_VERSION, FOLLOW_UP, ALTERNATIVE, SAME_PATTERN, CROSS_TECHNOLOGY
    notes = Column(String(255), nullable=True)

class QuestionHint(TimeStampedBase):
    __tablename__ = "question_hints"

    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    hint_level = Column(Integer, nullable=False) # 1: Conceptual, 2: Implementation, 3: Architecture
    hint_type = Column(String(50), nullable=False) # CONCEPTUAL, IMPLEMENTATION, ARCHITECTURE
    content = Column(Text, nullable=False)

    question = relationship("Question", back_populates="hints")

class QuestionSource(TimeStampedBase):
    __tablename__ = "question_sources"

    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    source_name = Column(String(255), nullable=False)
    source_url = Column(String(1000), nullable=True)
    publisher = Column(String(255), nullable=True)
    category = Column(String(100), default="Official Documentation", nullable=True)
    license = Column(String(100), default="Official Reference / Attribution", nullable=True)
    attribution_required = Column(Integer, default=1, nullable=False)

    question = relationship("Question", back_populates="sources")

class QuestionVersion(TimeStampedBase):
    __tablename__ = "question_versions"

    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, nullable=False)
    change_summary = Column(String(255), nullable=True)
    content_snapshot = Column(JSON, nullable=False)
    created_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    question = relationship("Question", back_populates="versions")

class QuestionFollowup(TimeStampedBase):
    __tablename__ = "question_followups"

    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    followup_question = Column(Text, nullable=False)
    answer_guidance = Column(Text, nullable=True)

    question = relationship("Question", back_populates="followups")
