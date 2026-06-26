"""推荐结果 schema"""

from pydantic import BaseModel
from typing import Optional


class SubjectMatch(BaseModel):
    """单科匹配详情"""
    subject: str
    student_score: float
    major_avg_score: Optional[float] = None
    major_min_score: Optional[float] = None
    diff: Optional[float] = None  # student - avg
    is_above_avg: bool = True
    hits_minimum: bool = True     # 是否达到最低要求


class MajorRecommendation(BaseModel):
    """单个专业推荐"""
    major_id: int
    major_name: str
    category: str
    subject_match_details: list[SubjectMatch]
    subject_adapt_score: float = 0  # 单科适配得分 (0-100)
    adapt_tags: list[str] = []      # 如 ["适配你的数学优势", "外语短板慎报"]
    risk_notes: list[str] = []      # 风险标注


class UniversityRecommendation(BaseModel):
    """单所院校推荐结果"""
    university_id: int
    university_name: str
    province: str
    city: str
    level: str
    is_public: bool
    tier: str  # "冲刺" / "稳妥" / "保底"

    # 位次匹配
    rank_match_score: float = 0     # 位次匹配度 (0-100)
    min_rank_3yr: list[int] = []    # 近三年最低位次

    # 单科适配
    subject_adapt_score: float = 0  # 综合单科适配度 (0-100)

    # 综合得分
    total_score: float = 0          # 综合推荐得分

    # 推荐专业列表
    recommended_majors: list[MajorRecommendation] = []

    # 院校标签
    tags: list[str] = []            # 如 ["985", "双一流", "工科强校"]
    risk_level: str = "low"         # "high" / "medium" / "low"


class RecommendResult(BaseModel):
    """完整推荐结果"""
    rush: list[UniversityRecommendation] = []     # 冲刺
    stable: list[UniversityRecommendation] = []   # 稳妥
    safe: list[UniversityRecommendation] = []     # 保底
    summary: dict = {}                            # 摘要统计
