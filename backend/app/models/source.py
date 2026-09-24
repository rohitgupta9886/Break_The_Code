from sqlalchemy import Column, String, Integer, Text, DateTime
from datetime import datetime, timezone
from app.models.base import TimeStampedBase

class ContentSource(TimeStampedBase):
    __tablename__ = "content_sources"

    title = Column(String(255), nullable=False)
    url = Column(String(1000), nullable=False, unique=True, index=True)
    source_type = Column(String(50), nullable=False, index=True) 
    # OFFICIAL_DOCUMENTATION, PRIMARY_ENGINEERING_SOURCE, INTERVIEW_EXPERIENCE, 
    # EDUCATIONAL_SOURCE, TECHNICAL_BLOG, GITHUB, COMMUNITY_SOURCE, OTHER
    
    publisher = Column(String(150), nullable=True)
    technology = Column(String(100), nullable=True, index=True)
    topic = Column(String(150), nullable=True)
    
    accessed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    last_verified_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    trust_level = Column(String(30), default="HIGH", nullable=False, index=True)
    # HIGH, MEDIUM, LOW, REQUIRES_REVIEW
    
    notes = Column(Text, nullable=True)
