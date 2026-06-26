"""专业模型"""

from sqlalchemy import Column, Integer, String, Float, Text, JSON, ForeignKey
from app.database import Base


class Major(Base):
    __tablename__ = "majors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False, index=True, comment="所属院校")
    name = Column(String(100), nullable=False, index=True, comment="专业名称")
    category = Column(String(50), comment="专业大类：工学/理学/医学/文学/经济学/管理学/法学/教育学/艺术学/农学")
    duration = Column(Integer, default=4, comment="学制（年）")
    degree = Column(String(30), comment="学位类型：工学/理学/医学/文学等")

    # 选科要求（新高考）
    subject_requirement = Column(String(200), comment="选科要求描述，如：物理+化学")
    subject_requirement_type = Column(String(50), comment="选科类型：3+1+2/3+3/传统文理")

    # 单科权重（核心差异化字段，JSON存储）
    # 格式：{"数学": 0.40, "物理": 0.30, "英语": 0.10, "语文": 0.10, "化学": 0.10}
    subject_weights = Column(JSON, comment="各单科在推荐中的权重")

    # 单科门槛
    min_subject_scores = Column(JSON, comment="单科最低分要求，如 {'英语': 110, '数学': 100}")

    # 就业与深造
    career_directions = Column(Text, comment="就业方向")
    civil_service_posts = Column(Text, comment="对应考公岗位")
    postgraduate_majors = Column(Text, comment="考研对口专业")
    suitable_for = Column(Text, comment="适合人群描述")
    warning = Column(Text, comment="劝退提醒")

    # 课程对应高中科目
    related_high_school_subjects = Column(Text, comment="对应高中科目")

    def __repr__(self):
        return f"<Major {self.name} @ university_id={self.university_id}>"
