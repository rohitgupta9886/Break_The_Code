from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RoleSchema(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class UserRead(UserBase):
    id: str
    is_active: bool
    is_verified: bool
    xp: int
    streak_days: int
    level: int = 1
    roles: List[RoleSchema] = []
    created_at: datetime
    last_active_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class AdminUserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: str = "USER" # USER or ADMIN
    is_active: bool = True

class AdminUserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

class BadgeRead(BaseModel):
    badge_key: str
    badge_name: str
    badge_description: str
    icon: str
    is_unlocked: bool = False
    unlocked_at: Optional[datetime] = None

class SRSReviewRequest(BaseModel):
    grade: int # 1 (Again), 2 (Hard), 3 (Good), 4 (Great), 5 (Easy)

class SRSCardRead(BaseModel):
    id: str
    question_id: str
    question_title: str
    question_slug: str
    technology_name: str
    difficulty: str
    repetitions: int
    interval_days: float
    ease_factor: float
    status: str
    next_review_at: datetime
    last_reviewed_at: Optional[datetime] = None
    last_score: Optional[float] = None
    is_due: bool = False

class TechProgressItem(BaseModel):
    technology_id: str
    name: str
    slug: str
    icon: str
    attempted: int
    completed: int
    accuracy_rate: float

class RecentAttemptItem(BaseModel):
    id: str
    question_id: str
    question_title: str
    question_slug: str
    technology_name: str
    difficulty: str
    score: float
    xp_earned: int
    time_spent_seconds: int
    created_at: datetime

class DashboardResponse(BaseModel):
    total_attempted: int
    total_completed: int
    overall_accuracy: float
    total_xp: int
    level: int
    xp_for_next_level: int
    current_level_progress_pct: float
    streak_days: int
    revision_due_count: int
    technologies_progress: List[TechProgressItem]
    recent_attempts: List[RecentAttemptItem]
    badges: List[BadgeRead]
    weak_topics: List[str]
    daily_challenge: Optional[dict] = None

