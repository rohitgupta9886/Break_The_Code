from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from app.models.base import TimeStampedBase, generate_uuid
from app.core.database import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", String(36), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", String(36), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", String(36), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)

class User(TimeStampedBase):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    xp = Column(Integer, default=0, nullable=False)
    streak_days = Column(Integer, default=0, nullable=False)
    last_active_date = Column(DateTime, nullable=True)

    roles = relationship("Role", secondary=user_roles, back_populates="users", lazy="selectin")
    attempts = relationship("UserAttempt", back_populates="user", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    revision_cards = relationship("SpacedRepetitionCard", back_populates="user", cascade="all, delete-orphan")
    badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")


class Role(TimeStampedBase):
    __tablename__ = "roles"

    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, lazy="selectin")

class Permission(TimeStampedBase):
    __tablename__ = "permissions"

    code = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
