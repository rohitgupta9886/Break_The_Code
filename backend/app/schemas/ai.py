from typing import List, Optional
from pydantic import BaseModel

class AnswerEvaluationRequest(BaseModel):
    question_id: str
    candidate_answer: str
    time_spent_seconds: Optional[int] = 0

class MetricScore(BaseModel):
    score: float # 0 to 10
    feedback: str

class AnswerEvaluationResponse(BaseModel):
    overall_score: float # 0 to 10
    correctness: MetricScore
    completeness: MetricScore
    technical_depth: MetricScore
    clarity: MetricScore
    covered_points: List[str]
    missed_points: List[str]
    improved_answer: str
    actionable_advice: str
    xp_earned: Optional[int] = 0
    streak_days: Optional[int] = None
    new_badges: Optional[List[str]] = []
    srs_interval_days: Optional[float] = None

class SocraticHintRequest(BaseModel):
    question_id: str
    candidate_thought: Optional[str] = None
    hint_level: int = 1 # 1: Conceptual, 2: Implementation, 3: Architecture

class SocraticHintResponse(BaseModel):
    hint_level: int
    hint_type: str
    socratic_question: str
    guiding_clue: str
