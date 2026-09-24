from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.base import TimeStampedBase, generate_uuid
from app.core.database import Base

class Answer(TimeStampedBase):
    __tablename__ = "answers"

    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    # 15-Part Structured Answer DNA
    direct_answer = Column(Text, nullable=True) # Elevator Pitch
    interview_ready_answer = Column(Text, nullable=False) # Spoken Verbal Answer
    deep_explanation = Column(Text, nullable=True) # Theoretical Mechanics
    example = Column(Text, nullable=True)
    architecture_notes = Column(Text, nullable=True)
    
    code = Column(Text, nullable=True)
    language = Column(String(50), default="python", nullable=True)
    algorithm = Column(String(100), nullable=True)
    time_complexity = Column(String(50), nullable=True)
    space_complexity = Column(String(50), nullable=True)
    
    edge_cases = Column(JSON, default=list, nullable=True)
    test_cases = Column(JSON, default=list, nullable=True)
    
    tradeoffs = Column(Text, nullable=True)
    production_considerations = Column(Text, nullable=True)
    failure_modes = Column(Text, nullable=True)
    common_mistakes = Column(JSON, default=list, nullable=True)
    follow_up_questions = Column(JSON, default=list, nullable=True)

    # Answer Lifecycle State Machine:
    # ANSWER_REQUIRED, GENERATING, GENERATED, VALIDATING, VALIDATED, NEEDS_REVIEW, REJECTED, REGENERATING, APPROVED, PUBLISHED, OUTDATED
    status = Column(String(30), default="VALIDATED", nullable=False, index=True)
    
    # Validation Status: NOT_VALIDATED, PASSED, FAILED, NEEDS_REVIEW
    validation_status = Column(String(30), default="PASSED", nullable=False, index=True)
    
    # Quality Scores
    overall_quality_score = Column(Float, default=0.94, nullable=False)
    completeness_score = Column(Float, default=0.95, nullable=False)
    correctness_score = Column(Float, default=0.95, nullable=False)
    relevance_score = Column(Float, default=0.96, nullable=False)
    depth_score = Column(Float, default=0.92, nullable=False)
    production_score = Column(Float, default=0.94, nullable=False)

    # Loop prevention and audit
    regeneration_attempt_count = Column(Integer, default=0, nullable=False)
    last_validated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    question = relationship("Question", back_populates="answer_record")
    validations = relationship("AnswerValidation", back_populates="answer", cascade="all, delete-orphan", order_by="desc(AnswerValidation.created_at)")


class AnswerValidation(TimeStampedBase):
    __tablename__ = "answer_validations"

    question_id = Column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    answer_id = Column(String(36), ForeignKey("answers.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Status: PASSED, FAILED, NEEDS_REVIEW
    status = Column(String(30), nullable=False, index=True)
    overall_score = Column(Float, default=0.0, nullable=False)
    
    # Detailed score breakdown (completeness, correctness, relevance, depth, code, production, sources)
    scores = Column(JSON, default=dict, nullable=False)
    
    # Detailed check results (existence, placeholder, structure, question_type, code_syntax, etc.)
    checks = Column(JSON, default=dict, nullable=False)
    
    # List of structured error items: [{code, severity, message, section}]
    errors = Column(JSON, default=list, nullable=False)
    warnings = Column(JSON, default=list, nullable=False)
    
    # Metadata
    validator_version = Column(String(20), default="1.0", nullable=False)
    is_publishable = Column(Boolean, default=False, nullable=False)
    validated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    notes = Column(Text, nullable=True)

    question = relationship("Question", back_populates="validations")
    answer = relationship("Answer", back_populates="validations")


class ValidationRuleConfig(TimeStampedBase):
    __tablename__ = "validation_rules"

    rule_key = Column(String(100), unique=True, nullable=False, index=True)
    rule_type = Column(String(50), nullable=False) # QUESTION_TYPE, DIFFICULTY, THRESHOLD
    configuration = Column(JSON, default=dict, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    description = Column(String(255), nullable=True)
