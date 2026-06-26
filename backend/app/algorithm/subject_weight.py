"""单科加权打分模块 —— 第二层核心差异化

根据考生的单科分数，结合专业对各科的权重设置，
计算单科适配度得分，并生成标签（优势/短板提示）。
"""

from app.schemas.recommendation import SubjectMatch
from app.schemas.student import StudentScoreInput


# 默认单科权重表（当专业没有自定义权重时使用）
DEFAULT_SUBJECT_WEIGHTS = {
    "理工类": {"数学": 0.35, "物理": 0.30, "英语": 0.15, "化学": 0.10, "语文": 0.10},
    "医学类": {"生物": 0.30, "化学": 0.30, "语文": 0.15, "英语": 0.15, "数学": 0.10},
    "文史类": {"语文": 0.40, "历史": 0.30, "英语": 0.15, "政治": 0.15},
    "经管类": {"数学": 0.40, "英语": 0.25, "语文": 0.15, "政治": 0.10, "历史": 0.10},
    "语言类": {"英语": 0.45, "语文": 0.35, "历史": 0.10, "政治": 0.10},
    "法学类": {"语文": 0.30, "政治": 0.30, "英语": 0.20, "历史": 0.20},
    "艺术类": {"语文": 0.40, "英语": 0.30, "历史": 0.30},
    "农学类": {"生物": 0.30, "化学": 0.30, "数学": 0.20, "物理": 0.10, "语文": 0.10},
}


# 分数段 -> 标签映射
def _score_level(score: float, full_mark: float = 150) -> str:
    """根据得分比例判定强/中/弱"""
    ratio = score / full_mark
    if ratio >= 0.85:
        return "strong"
    elif ratio >= 0.70:
        return "medium"
    else:
        return "weak"


def get_student_subject_map(score_input: StudentScoreInput) -> dict[str, float]:
    """将考生各科分数映射为标准字典"""
    mapping = {}
    if score_input.chinese is not None:
        mapping["语文"] = score_input.chinese
    if score_input.math is not None:
        mapping["数学"] = score_input.math
    if score_input.english is not None:
        mapping["英语"] = score_input.english
    if score_input.physics is not None:
        mapping["物理"] = score_input.physics
    if score_input.chemistry is not None:
        mapping["化学"] = score_input.chemistry
    if score_input.biology is not None:
        mapping["生物"] = score_input.biology
    if score_input.politics is not None:
        mapping["政治"] = score_input.politics
    if score_input.history is not None:
        mapping["历史"] = score_input.history
    if score_input.geography is not None:
        mapping["地理"] = score_input.geography
    return mapping


def compute_subject_adapt_score(
    student_scores: dict[str, float],
    subject_weights: dict[str, float] | None,
    category: str = "理工类",
) -> float:
    """
    计算单科加权适配度 (0-100)。

    将考生单科分数按比例映射到 0-100，再按专业权重加权求和。
    """
    weights = subject_weights or DEFAULT_SUBJECT_WEIGHTS.get(category, DEFAULT_SUBJECT_WEIGHTS["理工类"])
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 50.0

    weighted_score = 0.0
    for subj, weight in weights.items():
        raw = student_scores.get(subj)
        if raw is None:
            # 该科没有成绩，给中位分
            normalized = 50.0
        else:
            # 满分可能是150或100，按比例归一化
            full = 150 if subj in ("语文", "数学", "英语") else 100
            normalized = (raw / full) * 100
        weighted_score += normalized * (weight / total_weight)

    return round(weighted_score, 2)


def generate_subject_match_details(
    student_scores: dict[str, float],
    admission_avg: dict[str, float | None],
    admission_min: dict[str, float | None],
    subject_weights: dict[str, float] | None,
) -> list[SubjectMatch]:
    """
    生成逐科匹配详情。

    对比考生分数 vs 专业往年平均分 & 最低分。
    """
    details = []
    all_subjects = set(student_scores.keys()) | set(admission_avg.keys())

    for subj in sorted(all_subjects):
        stu_score = student_scores.get(subj)
        avg_score = admission_avg.get(subj)
        min_score = admission_min.get(subj)

        if stu_score is None:
            continue

        diff = (stu_score - avg_score) if avg_score is not None else None
        is_above = (diff >= 0) if diff is not None else True
        hits_min = (stu_score >= min_score) if min_score is not None else True

        details.append(SubjectMatch(
            subject=subj,
            student_score=stu_score,
            major_avg_score=avg_score,
            major_min_score=min_score,
            diff=round(diff, 1) if diff is not None else None,
            is_above_avg=is_above,
            hits_minimum=hits_min,
        ))
    return details


def generate_adapt_tags(
    student_scores: dict[str, float],
    subject_weights: dict[str, float] | None,
    category: str = "理工类",
) -> tuple[list[str], list[str]]:
    """
    生成适配标签和风险提示。

    Returns:
        (adapt_tags, risk_notes)
    """
    weights = subject_weights or DEFAULT_SUBJECT_WEIGHTS.get(category, DEFAULT_SUBJECT_WEIGHTS["理工类"])
    adapt_tags = []
    risk_notes = []

    for subj, weight in sorted(weights.items(), key=lambda x: -x[1]):
        raw = student_scores.get(subj)
        if raw is None:
            continue
        full = 150 if subj in ("语文", "数学", "英语") else 100
        level = _score_level(raw, full)

        if level == "strong" and weight >= 0.25:
            adapt_tags.append(f"适配你的{subj}优势")
        elif level == "weak" and weight >= 0.25:
            risk_notes.append(f"{subj}短板慎报（该专业重视{subj}）")

    return adapt_tags, risk_notes


def check_subject_minimums(
    student_scores: dict[str, float],
    min_subject_scores: dict[str, float] | None,
) -> list[str]:
    """检查是否达到专业单科最低分要求，返回不达标提示"""
    if not min_subject_scores:
        return []
    warnings = []
    for subj, min_score in min_subject_scores.items():
        raw = student_scores.get(subj)
        if raw is not None and raw < min_score:
            warnings.append(f"{subj}分数{raw}分，低于该专业最低要求{min_score}分")
    return warnings
