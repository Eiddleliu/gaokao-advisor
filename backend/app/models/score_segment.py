"""一分一段表 & 批次线"""

from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class ScoreSegment(Base):
    """一分一段表"""
    __tablename__ = "score_segments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    province = Column(String(50), nullable=False, index=True, comment="省份")
    year = Column(Integer, nullable=False, index=True, comment="年份")
    score = Column(Integer, nullable=False, comment="分数")
    count = Column(Integer, comment="本分人数")
    cumulative_count = Column(Integer, comment="累计人数（即该分数的位次）")
    exam_type = Column(String(20), comment="科类：物理类/历史类/理科/文科/综合")


class BatchLine(Base):
    """批次分数线"""
    __tablename__ = "batch_lines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    province = Column(String(50), nullable=False, index=True)
    year = Column(Integer, nullable=False)
    batch = Column(String(50), nullable=False, comment="批次名称")
    score = Column(Integer, nullable=False, comment="分数线")
    exam_type = Column(String(20), comment="科类")
