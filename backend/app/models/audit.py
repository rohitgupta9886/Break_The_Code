from sqlalchemy import Column, String, Integer, Text, JSON, DateTime, Float
from datetime import datetime, timezone
from app.models.base import TimeStampedBase

class AuditLog(TimeStampedBase):
    __tablename__ = "audit_logs"

    entity_type = Column(String(50), nullable=False, index=True) # QUESTION, SOURCE, TAXONOMY
    entity_id = Column(String(36), nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True) # GENERATED, TECHNICAL_REVIEW, APPROVED, PUBLISHED, EDITED, ARCHIVED
    actor_id = Column(String(36), nullable=True) # User ID or 'SYSTEM_AI'
    actor_role = Column(String(50), default="SYSTEM", nullable=False)
    details = Column(JSON, default=dict, nullable=True)
    notes = Column(Text, nullable=True)

class ContentGenerationJob(TimeStampedBase):
    __tablename__ = "content_generation_jobs"

    technology_slug = Column(String(100), nullable=False, index=True)
    target_difficulty = Column(String(50), nullable=False, index=True)
    target_count = Column(Integer, default=30, nullable=False)
    generated_count = Column(Integer, default=0, nullable=False)
    validated_count = Column(Integer, default=0, nullable=False)
    duplicate_count = Column(Integer, default=0, nullable=False)
    needs_review_count = Column(Integer, default=0, nullable=False)
    status = Column(String(30), default="PENDING", nullable=False, index=True) # PENDING, RUNNING, COMPLETED, FAILED
    progress_percentage = Column(Float, default=0.0, nullable=False)
    error_message = Column(Text, nullable=True)
    job_metadata = Column(JSON, default=dict, nullable=True)
