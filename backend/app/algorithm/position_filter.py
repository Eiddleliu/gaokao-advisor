"""位次筛选模块 —— 第一层过滤

根据考生全省位次，按冲/稳/保梯度筛选候选院校专业。
解决 "只看总分不准" 的问题，位次才是投档的核心依据。
"""

from app.config import settings


def get_rank_ranges(student_rank: int) -> dict[str, tuple[int, int]]:
    """
    根据考生位次计算冲/稳/保的位次区间。

    注意：位次越小越好（第1名 = 位次1）。
    - 冲刺：目标院校往年位次 < 考生位次（即更难的学校）
    - 稳妥：目标院校往年位次 ≈ 考生位次
    - 保底：目标院校往年位次 > 考生位次（即更容易的学校）

    Returns:
        {
            "rush":  (min_rank, max_rank),   -- 冲刺区间
            "stable": (min_rank, max_rank),  -- 稳妥区间
            "safe":   (min_rank, max_rank),  -- 保底区间
        }
    """
    return {
        "rush": (
            int(student_rank * settings.RUSH_RATIO_MIN),
            int(student_rank * settings.RUSH_RATIO_MAX),
        ),
        "stable": (
            int(student_rank * settings.STABLE_RATIO_MIN),
            int(student_rank * settings.STABLE_RATIO_MAX),
        ),
        "safe": (
            int(student_rank * settings.SAFE_RATIO_MIN),
            int(student_rank * settings.SAFE_RATIO_MAX),
        ),
    }


def classify_by_rank(
    target_min_rank: int,
    student_rank: int,
    ranges: dict[str, tuple[int, int]] | None = None,
) -> str | None:
    """
    判断目标院校专业属于冲/稳/保的哪一类。

    Args:
        target_min_rank: 该院校专业往年最低录取位次
        student_rank: 考生位次
        ranges: 预计算的位次区间

    Returns:
        "rush" / "stable" / "safe" / None（不在任何区间）
    """
    if ranges is None:
        ranges = get_rank_ranges(student_rank)

    for tier, (lo, hi) in ranges.items():
        if lo <= target_min_rank <= hi:
            return tier
    return None


def rank_match_score(target_min_rank: int, student_rank: int) -> float:
    """
    计算位次匹配得分 (0-100)。

    - 越接近考生位次得分越高
    - target < student（冲刺方向）得分递减
    - target > student（保底方向）得分递减
    """
    if student_rank == 0:
        return 0.0
    ratio = target_min_rank / student_rank
    if ratio < 0.5 or ratio > 1.8:
        return 0.0
    # 在 ratio=1.0 时达到最高分 100，两侧递减
    score = 100.0 * (1.0 - abs(ratio - 1.0) / 0.8)
    return max(0.0, min(100.0, score))
