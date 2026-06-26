"""模拟数据生成器

生成一套完整的模拟数据用于开发和演示，包含：
- 50 所模拟院校（涵盖 985/211/双一流/普通公办/民办）
- 每所院校 5-8 个专业
- 近 3 年录取数据（含单科平均分）
- 一分一段表
- 批次分数线
"""

import random
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, Base, async_session
from app.models import University, Major, AdmissionRecord, ScoreSegment, BatchLine, User


# ============= 模拟院校数据 =============

UNIVERSITIES = [
    # 985院校
    {"name": "清华大学", "province": "北京", "city": "北京", "level": "985", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.58, "employment_rate": 0.99, "avg_salary": 18000, "top_majors": "计算机科学与技术,电子信息,建筑学,机械工程,经济管理学院",
     "tuition_min": 5000, "tuition_max": 10000, "base_rank": 80, "base_score": 690},
    {"name": "北京大学", "province": "北京", "city": "北京", "level": "985", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.55, "employment_rate": 0.98, "avg_salary": 17500, "top_majors": "数学,物理学,化学,中文,经济学,法学",
     "tuition_min": 5000, "tuition_max": 8000, "base_rank": 90, "base_score": 688},
    {"name": "浙江大学", "province": "浙江", "city": "杭州", "level": "985", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.45, "employment_rate": 0.97, "avg_salary": 15000, "top_majors": "计算机科学与技术,控制科学,光学工程,电气工程,农学",
     "tuition_min": 5500, "tuition_max": 9000, "base_rank": 800, "base_score": 670},
    {"name": "上海交通大学", "province": "上海", "city": "上海", "level": "985", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.48, "employment_rate": 0.98, "avg_salary": 16000, "top_majors": "机械工程,船舶与海洋,电子信息,材料科学,临床医学",
     "tuition_min": 5500, "tuition_max": 10000, "base_rank": 500, "base_score": 675},
    {"name": "中国科学技术大学", "province": "安徽", "city": "合肥", "level": "985", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.50, "employment_rate": 0.96, "avg_salary": 14500, "top_majors": "物理学,化学,数学,天文学,量子信息",
     "tuition_min": 4800, "tuition_max": 7000, "base_rank": 1200, "base_score": 665},
    {"name": "南京大学", "province": "江苏", "city": "南京", "level": "985", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.42, "employment_rate": 0.96, "avg_salary": 14000, "top_majors": "天文学,地质学,物理学,化学,中文",
     "tuition_min": 5200, "tuition_max": 8000, "base_rank": 1800, "base_score": 660},
    {"name": "武汉大学", "province": "湖北", "city": "武汉", "level": "985", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.38, "employment_rate": 0.95, "avg_salary": 13000, "top_majors": "法学,遥感科学,水利工程,口腔医学,马克思主义理论",
     "tuition_min": 4500, "tuition_max": 8000, "base_rank": 3000, "base_score": 650},
    {"name": "华中科技大学", "province": "湖北", "city": "武汉", "level": "985", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.35, "employment_rate": 0.96, "avg_salary": 13500, "top_majors": "机械工程,光学工程,电气工程,计算机科学与技术,临床医学",
     "tuition_min": 4500, "tuition_max": 8000, "base_rank": 3500, "base_score": 648},
    {"name": "西安交通大学", "province": "陕西", "city": "西安", "level": "985", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.36, "employment_rate": 0.95, "avg_salary": 13000, "top_majors": "电气工程,动力工程,机械工程,管理科学,数学",
     "tuition_min": 4500, "tuition_max": 7500, "base_rank": 4500, "base_score": 642},
    {"name": "哈尔滨工业大学", "province": "黑龙江", "city": "哈尔滨", "level": "985", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.40, "employment_rate": 0.96, "avg_salary": 13500, "top_majors": "机械工程,控制科学,航天工程,计算机科学,焊接技术",
     "tuition_min": 4500, "tuition_max": 7000, "base_rank": 5000, "base_score": 640},

    # 211院校
    {"name": "南京航空航天大学", "province": "江苏", "city": "南京", "level": "211", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.22, "employment_rate": 0.95, "avg_salary": 12000, "top_majors": "航空宇航,机械工程,电子信息,计算机科学,自动化",
     "tuition_min": 5000, "tuition_max": 7000, "base_rank": 12000, "base_score": 615},
    {"name": "南京理工大学", "province": "江苏", "city": "南京", "level": "211", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.20, "employment_rate": 0.94, "avg_salary": 11500, "top_majors": "兵器科学,机械工程,电子信息,化学工程,自动化",
     "tuition_min": 5000, "tuition_max": 7000, "base_rank": 14000, "base_score": 610},
    {"name": "华东理工大学", "province": "上海", "city": "上海", "level": "211", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.22, "employment_rate": 0.94, "avg_salary": 12000, "top_majors": "化学工程,生物工程,材料科学,药学,环境工程",
     "tuition_min": 5000, "tuition_max": 8000, "base_rank": 15000, "base_score": 608},
    {"name": "武汉理工大学", "province": "湖北", "city": "武汉", "level": "211", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.18, "employment_rate": 0.93, "avg_salary": 11000, "top_majors": "材料科学,车辆工程,船舶工程,机械工程,交通工程",
     "tuition_min": 4500, "tuition_max": 7000, "base_rank": 18000, "base_score": 600},
    {"name": "北京交通大学", "province": "北京", "city": "北京", "level": "211", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.25, "employment_rate": 0.95, "avg_salary": 12500, "top_majors": "交通运输,通信工程,计算机科学,土木工程,经济管理",
     "tuition_min": 5000, "tuition_max": 7500, "base_rank": 10000, "base_score": 620},
    {"name": "上海财经大学", "province": "上海", "city": "上海", "level": "211", "type": "财经", "is_public": True,
     "postgraduate_rate": 0.28, "employment_rate": 0.96, "avg_salary": 15000, "top_majors": "会计学,金融学,经济学,统计学,国际商务",
     "tuition_min": 5000, "tuition_max": 8000, "base_rank": 8000, "base_score": 630},
    {"name": "中国政法大学", "province": "北京", "city": "北京", "level": "211", "type": "政法", "is_public": True,
     "postgraduate_rate": 0.30, "employment_rate": 0.94, "avg_salary": 13000, "top_majors": "法学,政治学,社会学,新闻学,经济学",
     "tuition_min": 5000, "tuition_max": 6000, "base_rank": 9000, "base_score": 625},
    {"name": "华中师范大学", "province": "湖北", "city": "武汉", "level": "211", "type": "师范", "is_public": True,
     "postgraduate_rate": 0.20, "employment_rate": 0.93, "avg_salary": 9500, "top_majors": "教育学,中文,历史学,数学,物理学",
     "tuition_min": 4000, "tuition_max": 6000, "base_rank": 20000, "base_score": 595},
    {"name": "西南大学", "province": "重庆", "city": "重庆", "level": "211", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.18, "employment_rate": 0.92, "avg_salary": 9000, "top_majors": "教育学,农学,心理学,中文,生物学",
     "tuition_min": 4000, "tuition_max": 6000, "base_rank": 25000, "base_score": 585},

    # 双一流（非211）
    {"name": "南京邮电大学", "province": "江苏", "city": "南京", "level": "双一流", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.15, "employment_rate": 0.94, "avg_salary": 12000, "top_majors": "通信工程,计算机科学,电子信息,信息安全,物联网",
     "tuition_min": 5000, "tuition_max": 7000, "base_rank": 22000, "base_score": 590},
    {"name": "成都中医药大学", "province": "四川", "city": "成都", "level": "双一流", "type": "医药", "is_public": True,
     "postgraduate_rate": 0.12, "employment_rate": 0.90, "avg_salary": 8500, "top_majors": "中医学,中药学,针灸推拿,中西医临床,护理学",
     "tuition_min": 4000, "tuition_max": 6000, "base_rank": 35000, "base_score": 565},
    {"name": "河南大学", "province": "河南", "city": "开封", "level": "双一流", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.14, "employment_rate": 0.91, "avg_salary": 8000, "top_majors": "中文,历史学,地理学,教育学,生物学",
     "tuition_min": 3800, "tuition_max": 5500, "base_rank": 40000, "base_score": 555},

    # 公办本科
    {"name": "山东科技大学", "province": "山东", "city": "青岛", "level": "公办本科", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.08, "employment_rate": 0.92, "avg_salary": 9000, "top_majors": "矿业工程,计算机科学,机械工程,安全工程,测绘",
     "tuition_min": 4500, "tuition_max": 6000, "base_rank": 55000, "base_score": 535},
    {"name": "青岛大学", "province": "山东", "city": "青岛", "level": "公办本科", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.10, "employment_rate": 0.91, "avg_salary": 8500, "top_majors": "临床医学,纺织工程,计算机科学,经济学,自动化",
     "tuition_min": 4500, "tuition_max": 6500, "base_rank": 50000, "base_score": 540},
    {"name": "济南大学", "province": "山东", "city": "济南", "level": "公办本科", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.08, "employment_rate": 0.90, "avg_salary": 8000, "top_majors": "材料科学,化学工程,计算机科学,水利工程,经济学",
     "tuition_min": 4500, "tuition_max": 6000, "base_rank": 65000, "base_score": 520},
    {"name": "山东师范大学", "province": "山东", "city": "济南", "level": "公办本科", "type": "师范", "is_public": True,
     "postgraduate_rate": 0.12, "employment_rate": 0.92, "avg_salary": 7500, "top_majors": "教育学,中文,数学,物理学,化学",
     "tuition_min": 4000, "tuition_max": 5500, "base_rank": 48000, "base_score": 545},
    {"name": "河北工业大学", "province": "天津", "city": "天津", "level": "211", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.18, "employment_rate": 0.93, "avg_salary": 10500, "top_majors": "电气工程,机械工程,材料科学,化学工程,土木工程",
     "tuition_min": 4500, "tuition_max": 6500, "base_rank": 28000, "base_score": 580},
    {"name": "天津医科大学", "province": "天津", "city": "天津", "level": "211", "type": "医药", "is_public": True,
     "postgraduate_rate": 0.25, "employment_rate": 0.95, "avg_salary": 10000, "top_majors": "临床医学,口腔医学,基础医学,预防医学,护理学",
     "tuition_min": 4500, "tuition_max": 6500, "base_rank": 16000, "base_score": 605},
    {"name": "杭州电子科技大学", "province": "浙江", "city": "杭州", "level": "公办本科", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.12, "employment_rate": 0.95, "avg_salary": 12000, "top_majors": "电子信息,计算机科学,自动化,通信工程,软件工程",
     "tuition_min": 5500, "tuition_max": 7000, "base_rank": 30000, "base_score": 575},
    {"name": "重庆邮电大学", "province": "重庆", "city": "重庆", "level": "公办本科", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.10, "employment_rate": 0.93, "avg_salary": 11000, "top_majors": "通信工程,计算机科学,信息安全,物联网,人工智能",
     "tuition_min": 4500, "tuition_max": 6500, "base_rank": 32000, "base_score": 570},

    # 民办本科
    {"name": "山东英才学院", "province": "山东", "city": "济南", "level": "民办本科", "type": "综合", "is_public": False,
     "postgraduate_rate": 0.02, "employment_rate": 0.85, "avg_salary": 5500, "top_majors": "学前教育,工商管理,计算机科学,护理学,会计学",
     "tuition_min": 15000, "tuition_max": 22000, "base_rank": 180000, "base_score": 445},
    {"name": "武昌理工学院", "province": "湖北", "city": "武汉", "level": "民办本科", "type": "理工", "is_public": False,
     "postgraduate_rate": 0.01, "employment_rate": 0.83, "avg_salary": 5000, "top_majors": "计算机科学,软件工程,土木工程,环境设计,工商管理",
     "tuition_min": 16000, "tuition_max": 24000, "base_rank": 190000, "base_score": 440},

    # 更多院校补充
    {"name": "山东大学", "province": "山东", "city": "济南", "level": "985", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.35, "employment_rate": 0.95, "avg_salary": 12500, "top_majors": "数学,中国语言文学,控制科学,临床医学,材料科学",
     "tuition_min": 4500, "tuition_max": 8000, "base_rank": 7000, "base_score": 635},
    {"name": "中国海洋大学", "province": "山东", "city": "青岛", "level": "985", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.28, "employment_rate": 0.93, "avg_salary": 11000, "top_majors": "海洋科学,水产,食品科学,环境科学,药学",
     "tuition_min": 4500, "tuition_max": 7000, "base_rank": 12000, "base_score": 615},
    {"name": "中国石油大学(华东)", "province": "山东", "city": "青岛", "level": "211", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.22, "employment_rate": 0.94, "avg_salary": 11500, "top_majors": "石油工程,地质资源,化学工程,机械工程,安全工程",
     "tuition_min": 4500, "tuition_max": 6500, "base_rank": 22000, "base_score": 590},
    {"name": "大连理工大学", "province": "辽宁", "city": "大连", "level": "985", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.32, "employment_rate": 0.95, "avg_salary": 13000, "top_majors": "化学工程,机械工程,力学,管理科学,水利工程",
     "tuition_min": 4500, "tuition_max": 7500, "base_rank": 6000, "base_score": 638},
    {"name": "中南大学", "province": "湖南", "city": "长沙", "level": "985", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.33, "employment_rate": 0.95, "avg_salary": 13000, "top_majors": "冶金工程,矿业工程,材料科学,临床医学,交通运输",
     "tuition_min": 4500, "tuition_max": 8000, "base_rank": 5500, "base_score": 640},
    {"name": "电子科技大学", "province": "四川", "city": "成都", "level": "985", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.38, "employment_rate": 0.97, "avg_salary": 15500, "top_majors": "电子信息,通信工程,计算机科学,光电技术,集成电路",
     "tuition_min": 4500, "tuition_max": 7000, "base_rank": 4000, "base_score": 648},
    {"name": "北京外国语大学", "province": "北京", "city": "北京", "level": "211", "type": "语言", "is_public": True,
     "postgraduate_rate": 0.28, "employment_rate": 0.95, "avg_salary": 13000, "top_majors": "英语,翻译,法语,德语,日语,国际关系",
     "tuition_min": 5000, "tuition_max": 6000, "base_rank": 8500, "base_score": 628},
    {"name": "同济大学", "province": "上海", "city": "上海", "level": "985", "type": "理工", "is_public": True,
     "postgraduate_rate": 0.42, "employment_rate": 0.97, "avg_salary": 15000, "top_majors": "建筑学,土木工程,城乡规划,交通运输,环境科学",
     "tuition_min": 5500, "tuition_max": 10000, "base_rank": 1500, "base_score": 662},
    {"name": "厦门大学", "province": "福建", "city": "厦门", "level": "985", "type": "综合", "is_public": True,
     "postgraduate_rate": 0.35, "employment_rate": 0.96, "avg_salary": 13500, "top_majors": "会计学,经济学,化学,海洋科学,统计学",
     "tuition_min": 5000, "tuition_max": 8000, "base_rank": 3800, "base_score": 647},
]


# ============= 专业模板 =============

MAJOR_TEMPLATES = {
    "理工": [
        {"name": "计算机科学与技术", "category": "工学", "duration": 4, "degree": "工学",
         "subject_weights": {"数学": 0.40, "物理": 0.30, "英语": 0.15, "语文": 0.15},
         "min_subject_scores": {"数学": 100}, "career_directions": "软件开发/算法工程师/数据科学家/AI研究员",
         "suitable_for": "逻辑思维强、喜欢编程和数学的学生", "related_high_school_subjects": "数学,物理"},
        {"name": "电子信息工程", "category": "工学", "duration": 4, "degree": "工学",
         "subject_weights": {"数学": 0.35, "物理": 0.35, "英语": 0.15, "化学": 0.15},
         "min_subject_scores": {"物理": 70}, "career_directions": "芯片设计/通信工程师/嵌入式开发",
         "suitable_for": "物理电学部分学得好、动手能力强的学生", "related_high_school_subjects": "数学,物理"},
        {"name": "机械工程", "category": "工学", "duration": 4, "degree": "工学",
         "subject_weights": {"数学": 0.35, "物理": 0.35, "化学": 0.15, "英语": 0.15},
         "min_subject_scores": None, "career_directions": "机械设计/制造工程师/汽车工程师",
         "suitable_for": "物理力学部分好、空间想象力强的学生", "related_high_school_subjects": "数学,物理"},
        {"name": "自动化", "category": "工学", "duration": 4, "degree": "工学",
         "subject_weights": {"数学": 0.40, "物理": 0.30, "英语": 0.15, "化学": 0.15},
         "min_subject_scores": {"数学": 90}, "career_directions": "控制工程师/机器人研发/工业自动化",
         "suitable_for": "数学好、喜欢动手和逻辑推理的学生", "related_high_school_subjects": "数学,物理"},
        {"name": "软件工程", "category": "工学", "duration": 4, "degree": "工学",
         "subject_weights": {"数学": 0.40, "英语": 0.25, "物理": 0.20, "语文": 0.15},
         "min_subject_scores": {"数学": 95}, "career_directions": "全栈开发/架构师/产品经理/技术管理",
         "suitable_for": "数学好、英语不差、喜欢编程的学生", "related_high_school_subjects": "数学"},
        {"name": "通信工程", "category": "工学", "duration": 4, "degree": "工学",
         "subject_weights": {"数学": 0.35, "物理": 0.35, "英语": 0.15, "语文": 0.15},
         "min_subject_scores": {"物理": 65}, "career_directions": "通信工程师/网络规划/5G研发",
         "suitable_for": "物理电学好、数学基础扎实的学生", "related_high_school_subjects": "数学,物理"},
        {"name": "土木工程", "category": "工学", "duration": 4, "degree": "工学",
         "subject_weights": {"数学": 0.30, "物理": 0.40, "化学": 0.15, "语文": 0.15},
         "min_subject_scores": None, "career_directions": "结构设计/施工管理/市政工程",
         "warning": "近年行业下行，就业环境较苦，建议谨慎选择", "suitable_for": "物理力学好、能吃苦的学生",
         "related_high_school_subjects": "数学,物理"},
        {"name": "材料科学与工程", "category": "工学", "duration": 4, "degree": "工学",
         "subject_weights": {"物理": 0.30, "化学": 0.35, "数学": 0.20, "英语": 0.15},
         "min_subject_scores": None, "career_directions": "材料研发/质检工程师/新能源材料",
         "warning": "本科就业面窄，多数需要读研", "suitable_for": "化学好、愿意深造的学生",
         "related_high_school_subjects": "化学,物理"},
    ],
    "医学": [
        {"name": "临床医学", "category": "医学", "duration": 5, "degree": "医学",
         "subject_weights": {"生物": 0.30, "化学": 0.30, "语文": 0.15, "英语": 0.15, "数学": 0.10},
         "min_subject_scores": {"化学": 75, "生物": 70},
         "career_directions": "临床医生/医学研究/公共卫生",
         "suitable_for": "生物化学好、有耐心、能承受长期学习压力的学生", "related_high_school_subjects": "生物,化学"},
        {"name": "口腔医学", "category": "医学", "duration": 5, "degree": "医学",
         "subject_weights": {"生物": 0.25, "化学": 0.25, "物理": 0.20, "数学": 0.15, "语文": 0.15},
         "min_subject_scores": {"化学": 70}, "career_directions": "口腔医生/正畸师/口腔修复",
         "suitable_for": "动手能力强、不怕血、细致耐心的学生", "related_high_school_subjects": "生物,化学"},
        {"name": "药学", "category": "医学", "duration": 4, "degree": "理学",
         "subject_weights": {"化学": 0.40, "生物": 0.25, "数学": 0.20, "英语": 0.15},
         "min_subject_scores": {"化学": 70}, "career_directions": "药物研发/药事管理/临床药师",
         "suitable_for": "化学特别好、对药物研究感兴趣的学生", "related_high_school_subjects": "化学,生物"},
    ],
    "经管": [
        {"name": "金融学", "category": "经济学", "duration": 4, "degree": "经济学",
         "subject_weights": {"数学": 0.40, "英语": 0.25, "语文": 0.15, "政治": 0.10, "历史": 0.10},
         "min_subject_scores": {"数学": 100}, "career_directions": "银行/证券/基金/投行/金融科技",
         "suitable_for": "数学好、对数字敏感、社交能力强的学生", "related_high_school_subjects": "数学"},
        {"name": "会计学", "category": "管理学", "duration": 4, "degree": "管理学",
         "subject_weights": {"数学": 0.35, "英语": 0.20, "语文": 0.25, "政治": 0.20},
         "min_subject_scores": None, "career_directions": "注册会计师/审计/财务管理/税务",
         "suitable_for": "细心、数学不差、愿意考证的学生", "related_high_school_subjects": "数学"},
        {"name": "经济学", "category": "经济学", "duration": 4, "degree": "经济学",
         "subject_weights": {"数学": 0.40, "英语": 0.20, "政治": 0.20, "语文": 0.10, "历史": 0.10},
         "min_subject_scores": {"数学": 95}, "career_directions": "经济分析师/政策研究/银行/咨询",
         "suitable_for": "数学好、对社会经济问题感兴趣的学生", "related_high_school_subjects": "数学"},
        {"name": "统计学", "category": "理学", "duration": 4, "degree": "理学",
         "subject_weights": {"数学": 0.50, "英语": 0.20, "物理": 0.15, "语文": 0.15},
         "min_subject_scores": {"数学": 110}, "career_directions": "数据分析师/精算师/生物统计/量化金融",
         "suitable_for": "数学特别好的学生，就业和考研都很好", "related_high_school_subjects": "数学"},
    ],
    "文史": [
        {"name": "汉语言文学", "category": "文学", "duration": 4, "degree": "文学",
         "subject_weights": {"语文": 0.50, "历史": 0.25, "英语": 0.15, "政治": 0.10},
         "min_subject_scores": {"语文": 100}, "career_directions": "教师/编辑/公务员/新媒体运营/文案策划",
         "suitable_for": "语文好、爱阅读写作、考公方向广的学生", "related_high_school_subjects": "语文,历史"},
        {"name": "法学", "category": "法学", "duration": 4, "degree": "法学",
         "subject_weights": {"语文": 0.30, "政治": 0.30, "英语": 0.20, "历史": 0.20},
         "min_subject_scores": {"语文": 90}, "career_directions": "律师/法官/检察官/公司法务/公务员",
         "warning": "通过法考是关键，竞争激烈但上限高", "suitable_for": "语文好、逻辑性强、有毅力的学生",
         "related_high_school_subjects": "语文,政治,历史"},
        {"name": "英语", "category": "文学", "duration": 4, "degree": "文学",
         "subject_weights": {"英语": 0.50, "语文": 0.25, "历史": 0.15, "政治": 0.10},
         "min_subject_scores": {"英语": 110}, "career_directions": "翻译/外贸/教师/国际组织/跨境电商",
         "warning": "纯语言就业面窄，建议辅修其他专业或考研", "suitable_for": "英语特别好、有跨文化兴趣的学生",
         "related_high_school_subjects": "英语"},
        {"name": "新闻学", "category": "文学", "duration": 4, "degree": "文学",
         "subject_weights": {"语文": 0.40, "英语": 0.20, "政治": 0.20, "历史": 0.20},
         "min_subject_scores": None, "career_directions": "记者/编辑/新媒体/公关/广告",
         "warning": "行业变化大，需要持续学习和跨界能力", "suitable_for": "语文好、关注社会、表达力强的学生",
         "related_high_school_subjects": "语文"},
    ],
    "师范": [
        {"name": "数学与应用数学", "category": "理学", "duration": 4, "degree": "理学",
         "subject_weights": {"数学": 0.55, "物理": 0.20, "语文": 0.15, "英语": 0.10},
         "min_subject_scores": {"数学": 105}, "career_directions": "数学教师/数据分析/精算/科研",
         "suitable_for": "数学特别好、愿意当老师或做研究的学生", "related_high_school_subjects": "数学"},
        {"name": "物理学", "category": "理学", "duration": 4, "degree": "理学",
         "subject_weights": {"物理": 0.45, "数学": 0.30, "英语": 0.15, "化学": 0.10},
         "min_subject_scores": {"物理": 75}, "career_directions": "物理教师/科研/光电行业/量子计算",
         "warning": "本科就业面窄，多数需读研", "suitable_for": "物理特别好、有科研兴趣的学生",
         "related_high_school_subjects": "物理,数学"},
        {"name": "生物科学", "category": "理学", "duration": 4, "degree": "理学",
         "subject_weights": {"生物": 0.40, "化学": 0.30, "数学": 0.15, "英语": 0.15},
         "min_subject_scores": {"生物": 70}, "career_directions": "生物教师/生物医药/基因研究/农业",
         "warning": "本科就业难，强烈建议读研", "suitable_for": "生物化学好、对生命科学有兴趣的学生",
         "related_high_school_subjects": "生物,化学"},
    ],
}


def _generate_major_for_university(uni_type: str) -> list[dict]:
    """根据院校类型生成专业列表"""
    majors = []

    # 根据院校类型选择专业模板
    if uni_type == "理工":
        majors.extend(random.sample(MAJOR_TEMPLATES["理工"], min(6, len(MAJOR_TEMPLATES["理工"]))))
        majors.extend(random.sample(MAJOR_TEMPLATES["经管"], min(2, len(MAJOR_TEMPLATES["经管"]))))
        majors.extend(random.sample(MAJOR_TEMPLATES["师范"], min(1, len(MAJOR_TEMPLATES["师范"]))))
    elif uni_type == "综合":
        majors.extend(random.sample(MAJOR_TEMPLATES["理工"], min(3, len(MAJOR_TEMPLATES["理工"]))))
        majors.extend(random.sample(MAJOR_TEMPLATES["经管"], min(2, len(MAJOR_TEMPLATES["经管"]))))
        majors.extend(random.sample(MAJOR_TEMPLATES["文史"], min(2, len(MAJOR_TEMPLATES["文史"]))))
        majors.extend(random.sample(MAJOR_TEMPLATES["师范"], min(1, len(MAJOR_TEMPLATES["师范"]))))
    elif uni_type == "医药":
        majors.extend(random.sample(MAJOR_TEMPLATES["医学"], min(3, len(MAJOR_TEMPLATES["医学"]))))
        majors.extend(random.sample(MAJOR_TEMPLATES["师范"], min(1, len(MAJOR_TEMPLATES["师范"]))))
    elif uni_type == "财经":
        majors.extend(MAJOR_TEMPLATES["经管"])
        majors.extend(random.sample(MAJOR_TEMPLATES["文史"], min(1, len(MAJOR_TEMPLATES["文史"]))))
    elif uni_type == "政法":
        majors.extend(MAJOR_TEMPLATES["文史"])
        majors.extend(random.sample(MAJOR_TEMPLATES["经管"], min(1, len(MAJOR_TEMPLATES["经管"]))))
    elif uni_type == "师范":
        majors.extend(MAJOR_TEMPLATES["师范"])
        majors.extend(random.sample(MAJOR_TEMPLATES["文史"], min(2, len(MAJOR_TEMPLATES["文史"]))))
        majors.extend(random.sample(MAJOR_TEMPLATES["理工"], min(1, len(MAJOR_TEMPLATES["理工"]))))
    elif uni_type == "语言":
        majors.extend(MAJOR_TEMPLATES["文史"])
    else:
        majors.extend(random.sample(MAJOR_TEMPLATES["理工"], min(3, len(MAJOR_TEMPLATES["理工"]))))
        majors.extend(random.sample(MAJOR_TEMPLATES["经管"], min(2, len(MAJOR_TEMPLATES["经管"]))))

    return majors


def _generate_admission_data(
    base_score: int, base_rank: int, major_category: str, year: int,
) -> dict:
    """生成一条录取数据的单科分数"""
    year_offset = random.randint(-5, 5)  # 年际波动
    adjusted_score = base_score + year_offset + random.randint(-8, 8)
    adjusted_rank = max(1, base_rank + random.randint(-int(base_rank * 0.08), int(base_rank * 0.08)))

    # 根据专业类别生成不同分布的单科平均分
    if major_category in ("工学", "理学"):
        avg_math = random.gauss(120, 12)
        avg_physics = random.gauss(78, 10)
        avg_chemistry = random.gauss(75, 10)
        avg_english = random.gauss(110, 12)
        avg_chinese = random.gauss(105, 8)
        avg_biology = random.gauss(72, 10)
    elif major_category in ("医学",):
        avg_math = random.gauss(110, 10)
        avg_physics = random.gauss(70, 10)
        avg_chemistry = random.gauss(82, 8)
        avg_biology = random.gauss(80, 8)
        avg_english = random.gauss(108, 12)
        avg_chinese = random.gauss(108, 8)
    elif major_category in ("经济学", "管理学"):
        avg_math = random.gauss(125, 10)
        avg_english = random.gauss(118, 10)
        avg_chinese = random.gauss(110, 8)
        avg_physics = random.gauss(70, 10)
        avg_chemistry = random.gauss(68, 10)
        avg_biology = random.gauss(65, 10)
    elif major_category in ("文学", "法学"):
        avg_math = random.gauss(105, 12)
        avg_english = random.gauss(120, 10)
        avg_chinese = random.gauss(118, 8)
        avg_history = random.gauss(80, 8)
        avg_politics = random.gauss(78, 8)
        avg_physics = None
        avg_chemistry = None
        avg_biology = None
    else:
        avg_math = random.gauss(110, 12)
        avg_english = random.gauss(110, 12)
        avg_chinese = random.gauss(108, 8)
        avg_physics = random.gauss(72, 10)
        avg_chemistry = random.gauss(70, 10)
        avg_biology = random.gauss(68, 10)

    def clamp(val, lo, hi):
        if val is None:
            return None
        return max(lo, min(hi, round(val)))

    return {
        "min_total_score": adjusted_score - random.randint(3, 8),
        "avg_total_score": adjusted_score,
        "min_rank": adjusted_rank + random.randint(0, int(adjusted_rank * 0.05)),
        "avg_rank": adjusted_rank,
        "avg_chinese": clamp(locals().get("avg_chinese"), 85, 135),
        "avg_math": clamp(locals().get("avg_math"), 80, 148),
        "avg_english": clamp(locals().get("avg_english"), 80, 145),
        "avg_physics": clamp(locals().get("avg_physics"), 50, 98),
        "avg_chemistry": clamp(locals().get("avg_chemistry"), 50, 98),
        "avg_biology": clamp(locals().get("avg_biology"), 50, 98),
        "avg_politics": clamp(locals().get("avg_politics", None), 55, 95),
        "avg_history": clamp(locals().get("avg_history", None), 55, 95),
        "avg_geography": clamp(locals().get("avg_geography", None), 55, 95),
        "min_math": clamp((locals().get("avg_math") or 110) - 20, 60, 140),
        "min_english": clamp((locals().get("avg_english") or 110) - 15, 70, 130),
        "min_physics": clamp((locals().get("avg_physics") or 70) - 15, 40, 90),
        "plan_count": random.randint(20, 120),
        "admitted_count": random.randint(18, 115),
    }


async def seed_database():
    """填充数据库"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        print("[INFO] 开始生成模拟数据...")

        # 创建测试用户
        user = User(username="demo", email="demo@test.com", province="山东", exam_type="新高考3+3")
        db.add(user)

        for uni_data in UNIVERSITIES:
            base_rank = uni_data.pop("base_rank")
            base_score = uni_data.pop("base_score")

            uni = University(**uni_data)
            db.add(uni)
            await db.flush()

            # 生成专业
            major_templates = _generate_major_for_university(uni.type or "综合")
            for mt in major_templates:
                major = Major(
                    university_id=uni.id,
                    name=mt["name"],
                    category=mt.get("category"),
                    duration=mt.get("duration", 4),
                    degree=mt.get("degree"),
                    subject_requirement="物理+化学" if mt.get("category") in ("工学", "理学", "医学") else "不限",
                    subject_requirement_type="3+3",
                    subject_weights=mt.get("subject_weights"),
                    min_subject_scores=mt.get("min_subject_scores"),
                    career_directions=mt.get("career_directions"),
                    suitable_for=mt.get("suitable_for"),
                    warning=mt.get("warning"),
                    related_high_school_subjects=mt.get("related_high_school_subjects"),
                )
                db.add(major)
                await db.flush()

                # 生成3年录取数据
                for year in [2023, 2024, 2025]:
                    adm_data = _generate_admission_data(
                        base_score, base_rank, major.category, year,
                    )
                    record = AdmissionRecord(
                        university_id=uni.id,
                        major_id=major.id,
                        province="山东",
                        year=year,
                        batch="本科批",
                        **adm_data,
                    )
                    db.add(record)

        # 生成一分一段表（山东省 2025，简化版）
        print("[INFO] 生成一分一段表...")
        cum = 0
        for score in range(750, 300, -1):
            # 模拟正态分布
            import math
            mean, std = 500, 100
            count = int(800000 * (1 / (std * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((score - mean) / std) ** 2))
            count = max(1, count)
            cum += count
            seg = ScoreSegment(
                province="山东", year=2025, score=score,
                count=count, cumulative_count=cum, exam_type="综合",
            )
            db.add(seg)

        # 批次线
        for batch, score in [("特殊类型批", 521), ("普通一段", 444), ("普通二段", 150)]:
            db.add(BatchLine(province="山东", year=2025, batch=batch, score=score, exam_type="综合"))

        await db.commit()
        print(f"[OK] 数据生成完成! {len(UNIVERSITIES)} 所院校，含录取数据。")


if __name__ == "__main__":
    asyncio.run(seed_database())
