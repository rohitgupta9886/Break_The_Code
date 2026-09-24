from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedBase

class Domain(TimeStampedBase):
    __tablename__ = "domains"

    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    order_index = Column(Integer, default=0, nullable=False)

    technologies = relationship("Technology", back_populates="domain", cascade="all, delete-orphan", lazy="selectin")

class Technology(TimeStampedBase):
    __tablename__ = "technologies"

    domain_id = Column(String(36), ForeignKey("domains.id", ondelete="CASCADE"), nullable=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    short_description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    order_index = Column(Integer, default=0, nullable=False)

    domain = relationship("Domain", back_populates="technologies")
    topics = relationship("Topic", back_populates="technology", cascade="all, delete-orphan", lazy="selectin")
    questions = relationship("Question", back_populates="technology", cascade="all, delete-orphan")

class Topic(TimeStampedBase):
    __tablename__ = "topics"

    technology_id = Column(String(36), ForeignKey("technologies.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0, nullable=False)

    technology = relationship("Technology", back_populates="topics")
    questions = relationship("Question", back_populates="topic")

class Tag(TimeStampedBase):
    __tablename__ = "tags"

    name = Column(String(50), unique=True, index=True, nullable=False)
    slug = Column(String(50), unique=True, index=True, nullable=False)
