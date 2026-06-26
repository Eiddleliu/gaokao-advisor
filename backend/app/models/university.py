"""院校模型"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, JSON
from app.database import Base


class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True, comment="院校名称")
    province = Column(String(50), comment="所在省份")
    city = Column(String(50), comment="所在城市")
    level = Column(String(50), comment="层次：985/211/双一流/公办本科/民办本科/公办专科")
    type = Column(String(50), comment="类型：综合/理工/师范/医药/财经/政法/农林/艺术/军事")
    is_public = Column(Boolean, default=True, comment="是否公办")

    # 招生信息
    enrollment_plan_count = Column(Integer, comment="当年招生计划人数")
    tuition_min = Column(Float, comment="最低学费（元/年）")
    tuition_max = Column(Float, comment="最高学费（元/年）")

    # 就业与深造
    postgraduate_rate = Column(Float, comment="保研率")
    employment_rate = Column(Float, comment="就业率")
    avg_salary = Column(Float, comment="毕业生平均薪资")
    top_majors = Column(Text, comment="王牌专业，逗号分隔")

    # 附加信息
    description = Column(Text, comment="院校简介")
    website = Column(String(255), comment="官网")

    def __repr__(self):
        return f"<University {self.name}>"
