"""录取数据模型 —— 包含总分 + 单科平均分（核心差异化数据）"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class AdmissionRecord(Base):
    __tablename__ = "admission_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False, index=True)
    major_id = Column(Integer, ForeignKey("majors.id"), nullable=False, index=True)
    province = Column(String(50), nullable=False, comment="生源省份")
    year = Column(Integer, nullable=False, comment="录取年份")
    batch = Column(String(50), comment="录取批次：一本/二本/本科批/专科批")

    # 总分录取数据
    min_total_score = Column(Float, comment="最低录取总分")
    avg_total_score = Column(Float, comment="平均录取总分")
    min_rank = Column(Integer, comment="最低录取位次")
    avg_rank = Column(Integer, comment="平均录取位次")

    # 单科录取平均分（核心差异化数据）
    avg_chinese = Column(Float, comment="语文录取平均分")
    avg_math = Column(Float, comment="数学录取平均分")
    avg_english = Column(Float, comment="英语录取平均分")
    avg_physics = Column(Float, comment="物理录取平均分")
    avg_chemistry = Column(Float, comment="化学录取平均分")
    avg_biology = Column(Float, comment="生物录取平均分")
    avg_politics = Column(Float, comment="政治录取平均分")
    avg_history = Column(Float, comment="历史录取平均分")
    avg_geography = Column(Float, comment="地理录取平均分")
    avg_comprehensive_science = Column(Float, comment="理综平均分（传统高考）")
    avg_comprehensive_arts = Column(Float, comment="文综平均分（传统高考）")

    # 单科最低控制线
    min_chinese = Column(Float, comment="语文最低分")
    min_math = Column(Float, comment="数学最低分")
    min_english = Column(Float, comment="英语最低分")
    min_physics = Column(Float, comment="物理最低分")
    min_chemistry = Column(Float, comment="化学最低分")
    min_biology = Column(Float, comment="生物最低分")

    # 计划与录取人数
    plan_count = Column(Integer, comment="招生计划人数")
    admitted_count = Column(Integer, comment="实际录取人数")

    def __repr__(self):
        return f"<AdmissionRecord uni={self.university_id} major={self.major_id} {self.year} {self.province}>"
