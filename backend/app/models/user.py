"""用户 & 志愿方案模型"""

from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100))
    province = Column(String(50))
    exam_type = Column(String(30), comment="高考类型：新高考3+1+2/3+3/传统文理")
    created_at = Column(DateTime, server_default=func.now())


class StudentScore(Base):
    """考生成绩记录"""
    __tablename__ = "student_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    province = Column(String(50), nullable=False)
    exam_type = Column(String(30), nullable=False)
    year = Column(Integer, nullable=False)

    # 总分与位次
    total_score = Column(Float, nullable=False)
    rank = Column(Integer, comment="全省位次")

    # 单科分数
    chinese = Column(Float, comment="语文")
    math = Column(Float, comment="数学")
    english = Column(Float, comment="英语")
    physics = Column(Float, comment="物理")
    chemistry = Column(Float, comment="化学")
    biology = Column(Float, comment="生物")
    politics = Column(Float, comment="政治")
    history = Column(Float, comment="历史")
    geography = Column(Float, comment="地理")
    comprehensive_science = Column(Float, comment="理综")
    comprehensive_arts = Column(Float, comment="文综")

    # 偏好标签
    preferences = Column(JSON, comment="偏好标签：城市、公办/民办、学费上限等")
    created_at = Column(DateTime, server_default=func.now())


class VolunteerPlan(Base):
    """志愿方案"""
    __tablename__ = "volunteer_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    score_id = Column(Integer, ForeignKey("student_scores.id"), nullable=False)
    name = Column(String(100), comment="方案名称，如：冲名校优先/专业适配优先/稳妥保底优先")
    strategy = Column(String(50), comment="策略类型：rush/major_fit/safe/custom")
    choices = Column(JSON, comment="志愿选项列表 [{university_id, major_id, order, is_adjust}]")
    risk_notes = Column(JSON, comment="风险标注")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Favorite(Base):
    """收藏的院校/专业"""
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    target_type = Column(String(20), comment="university / major")
    target_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
