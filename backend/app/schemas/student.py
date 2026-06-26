"""考生成绩 & 推荐请求的 Pydantic schema"""

from pydantic import BaseModel, Field
from typing import Optional


class StudentScoreInput(BaseModel):
    """考生信息录入"""
    province: str = Field(..., description="省份")
    exam_type: str = Field(..., description="高考类型：新高考3+1+2/3+3/传统文理")
    batch: str = Field("本科批", description="批次")
    year: int = Field(2026, description="高考年份")

    # 总分 & 位次
    total_score: float = Field(..., ge=0, le=750, description="总分")
    rank: int = Field(..., ge=1, description="全省位次")

    # 单科分数
    chinese: Optional[float] = Field(None, ge=0, le=150, description="语文")
    math: Optional[float] = Field(None, ge=0, le=150, description="数学")
    english: Optional[float] = Field(None, ge=0, le=150, description="英语")
    physics: Optional[float] = Field(None, ge=0, le=100, description="物理")
    chemistry: Optional[float] = Field(None, ge=0, le=100, description="化学")
    biology: Optional[float] = Field(None, ge=0, le=100, description="生物")
    politics: Optional[float] = Field(None, ge=0, le=100, description="政治")
    history: Optional[float] = Field(None, ge=0, le=100, description="历史")
    geography: Optional[float] = Field(None, ge=0, le=100, description="地理")
    comprehensive_science: Optional[float] = Field(None, ge=0, le=300, description="理综")
    comprehensive_arts: Optional[float] = Field(None, ge=0, le=300, description="文综")

    # 偏好
    city_preference: Optional[list[str]] = Field(None, description="城市偏好")
    public_only: Optional[bool] = Field(None, description="只看公办")
    max_tuition: Optional[float] = Field(None, description="学费上限")
    accept_adjustment: Optional[bool] = Field(True, description="是否接受调剂")
    excluded_majors: Optional[list[str]] = Field(None, description="排除的专业大类")
    career_goal: Optional[str] = Field(None, description="长期规划：考研/考公/就业/出国")
    special_type: Optional[str] = Field(None, description="特殊类型：强基/艺考/单招/军警/公费师范")


class RecommendRequest(BaseModel):
    """推荐请求"""
    score: StudentScoreInput
    strategy: str = Field("balanced", description="策略：balanced/rush_first/major_fit/safe_first")
    limit: int = Field(30, ge=1, le=100, description="每类返回数量上限")
