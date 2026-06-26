"""院校相关 schema"""

from pydantic import BaseModel
from typing import Optional


class UniversityDetail(BaseModel):
    id: int
    name: str
    province: str
    city: str
    level: str
    type: str
    is_public: bool
    tuition_min: Optional[float] = None
    tuition_max: Optional[float] = None
    postgraduate_rate: Optional[float] = None
    employment_rate: Optional[float] = None
    avg_salary: Optional[float] = None
    top_majors: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class MajorDetail(BaseModel):
    id: int
    university_id: int
    name: str
    category: str
    duration: int
    degree: Optional[str] = None
    subject_requirement: Optional[str] = None
    subject_weights: Optional[dict] = None
    min_subject_scores: Optional[dict] = None
    career_directions: Optional[str] = None
    suitable_for: Optional[str] = None
    warning: Optional[str] = None

    class Config:
        from_attributes = True


class UniversityListQuery(BaseModel):
    province: Optional[str] = None
    city: Optional[str] = None
    level: Optional[str] = None
    type: Optional[str] = None
    keyword: Optional[str] = None
    page: int = 1
    page_size: int = 20
