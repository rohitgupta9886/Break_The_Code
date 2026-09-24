from typing import Optional, List, Any
from pydantic import BaseModel
from datetime import datetime

class QuestionHintSchema(BaseModel):
    id: str
    hint_level: int
    hint_type: str
    content: str

    class Config:
        from_attributes = True

class QuestionSourceSchema(BaseModel):
    source_name: str
    source_url: Optional[str] = None
    license: Optional[str] = None
    attribution_required: int = 1
    publisher: Optional[str] = None
    category: Optional[str] = "Official Documentation"

    class Config:
        from_attributes = True

class QuestionFollowupSchema(BaseModel):
    id: str
    followup_question: str
    answer_guidance: Optional[str] = None

    class Config:
        from_attributes = True

class TagSchema(BaseModel):
    name: str
    slug: str

    class Config:
        from_attributes = True

class QuestionCardSchema(BaseModel):
    id: str
    slug: str
    title: str
    difficulty: str
    interview_depth: str
    question_type: str
    estimated_time_minutes: int
    role_target: Optional[str] = "Software Engineer"
    interview_round: Optional[str] = "Technical Screen"
    technology_name: Optional[str] = None
    technology_slug: Optional[str] = None
    topic_name: Optional[str] = None
    view_count: int = 0
    upvote_count: int = 0
    status: str
    tags: List[TagSchema] = []
    created_at: datetime

    class Config:
        from_attributes = True

class QuestionDetailSchema(BaseModel):
    id: str
    slug: str
    title: str
    difficulty: str
    interview_depth: str
    question_type: str
    role_target: Optional[str] = "Software Engineer"
    experience_level: Optional[str] = "All Levels"
    interview_round: Optional[str] = "Technical Screen"
    estimated_time_minutes: int
    
    short_answer: Optional[str] = None
    interview_ready_answer: str
    deep_explanation: Optional[str] = None
    architecture_notes: Optional[str] = None
    code_example: Optional[str] = None
    common_mistakes: Optional[List[Any]] = []
    why_interviewer_asks: Optional[str] = None
    interviewer_intent: Optional[str] = None
    
    status: str
    content_origin: str
    view_count: int
    upvote_count: int
    created_at: datetime
    last_reviewed_at: datetime
    
    technology_name: Optional[str] = None
    technology_slug: Optional[str] = None
    topic_name: Optional[str] = None
    
    hints: List[QuestionHintSchema] = []
    sources: List[QuestionSourceSchema] = []
    followups: List[QuestionFollowupSchema] = []
    tags: List[TagSchema] = []

    class Config:
        from_attributes = True

class QuestionCreateSchema(BaseModel):
    title: str
    slug: Optional[str] = None
    technology_id: str
    topic_id: Optional[str] = None
    difficulty: str = "MEDIUM" # BASIC, MEDIUM, TOUGH
    interview_depth: str = "L2" # L1, L2, L3, L4, L5
    question_type: str = "CONCEPTUAL"
    role_target: Optional[str] = "Software Engineer"
    experience_level: Optional[str] = "Mid"
    estimated_time_minutes: int = 5
    short_answer: Optional[str] = None
    interview_ready_answer: str
    deep_explanation: Optional[str] = None
    architecture_notes: Optional[str] = None
    code_example: Optional[str] = None
    common_mistakes: Optional[List[str]] = []
    interviewer_intent: Optional[str] = None
    status: str = "PUBLISHED"
    content_origin: str = "ORIGINAL"
    hints: Optional[List[dict]] = []
    sources: Optional[List[dict]] = []
    followups: Optional[List[dict]] = []
    tags: Optional[List[str]] = []

class QuestionFilterParams(BaseModel):
    technology: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    interview_depth: Optional[str] = None
    question_type: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    limit: int = 20

class QuestionUpdateSchema(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    technology_id: Optional[str] = None
    topic_id: Optional[str] = None
    difficulty: Optional[str] = None
    interview_depth: Optional[str] = None
    question_type: Optional[str] = None
    role_target: Optional[str] = None
    experience_level: Optional[str] = None
    interview_round: Optional[str] = None
    estimated_time_minutes: Optional[int] = None
    short_answer: Optional[str] = None
    interview_ready_answer: Optional[str] = None
    deep_explanation: Optional[str] = None
    architecture_notes: Optional[str] = None
    code_example: Optional[str] = None
    why_interviewer_asks: Optional[str] = None
    interviewer_intent: Optional[str] = None
    production_considerations: Optional[str] = None
    failure_modes: Optional[str] = None
    tradeoffs: Optional[str] = None
    common_mistakes: Optional[List[str]] = None
    status: Optional[str] = None
    content_origin: Optional[str] = None
    hints: Optional[List[dict]] = None
    sources: Optional[List[dict]] = None
    followups: Optional[List[dict]] = None
    tags: Optional[List[str]] = None

class QuestionStatusUpdateSchema(BaseModel):
    status: str
    note: Optional[str] = None

