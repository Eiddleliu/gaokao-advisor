from app.models.university import University
from app.models.major import Major
from app.models.admission import AdmissionRecord
from app.models.score_segment import ScoreSegment, BatchLine
from app.models.user import User, StudentScore, VolunteerPlan, Favorite

__all__ = [
    "University", "Major", "AdmissionRecord",
    "ScoreSegment", "BatchLine",
    "User", "StudentScore", "VolunteerPlan", "Favorite",
]
