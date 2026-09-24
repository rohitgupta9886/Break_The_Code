from typing import Optional, List
from pydantic import BaseModel

class TopicBase(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    order_index: int = 0

    class Config:
        from_attributes = True

class TechnologyBase(BaseModel):
    id: str
    name: str
    slug: str
    short_description: Optional[str] = None
    icon: Optional[str] = None
    is_active: bool = True
    order_index: int = 0
    question_count: Optional[int] = 0
    topics: List[TopicBase] = []

    class Config:
        from_attributes = True

class DomainWithTechnologies(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None
    technologies: List[TechnologyBase] = []

    class Config:
        from_attributes = True
