"""推荐引擎主模块 —— 组合位次筛选 + 单科加权

完整推荐流程：
1. 从数据库查询候选院校专业（按位次区间初筛）
2. 对每个候选计算位次匹配得分
3. 对每个候选计算单科适配度得分
4. 综合加权排序，按冲/稳/保分组
5. 生成标签、风险提示
"""

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import University, Major, AdmissionRecord
from app.schemas.student import StudentScoreInput, RecommendRequest
from app.schemas.recommendation import (
    MajorRecommendation, UniversityRecommendation, RecommendResult,
)
from app.algorithm.position_filter import (
    get_rank_ranges, classify_by_rank, rank_match_score,
)
from app.algorithm.subject_weight import (
    get_student_subject_map, compute_subject_adapt_score,
    generate_subject_match_details, generate_adapt_tags,
    check_subject_minimums,
)


# 综合得分中位次与单科的权重
RANK_WEIGHT = 0.45
SUBJECT_WEIGHT = 0.55


async def get_recommendations(
    db: AsyncSession,
    request: RecommendRequest,
) -> RecommendResult:
    """
    完整推荐流程入口。
    """
    score = request.score
    student_scores = get_student_subject_map(score)
    rank_ranges = get_rank_ranges(score.rank)

    # 1. 查询所有候选录取记录（最近3年，同省）
    recent_years = [2023, 2024, 2025]
    stmt = (
        select(AdmissionRecord, University, Major)
        .join(University, AdmissionRecord.university_id == University.id)
        .join(Major, AdmissionRecord.major_id == Major.id)
        .where(
            and_(
                AdmissionRecord.province == score.province,
                AdmissionRecord.year.in_(recent_years),
            )
        )
    )

    # 偏好过滤
    if score.public_only:
        stmt = stmt.where(University.is_public == True)
    if score.city_preference:
        stmt = stmt.where(University.city.in_(score.city_preference))
    if score.max_tuition:
        stmt = stmt.where(University.tuition_max <= score.max_tuition)

    result = await db.execute(stmt)
    rows = result.all()

    # 2. 按院校聚合（取最近一年的位次做初筛）
    uni_data: dict[int, dict] = {}
    for record, university, major in rows:
        uid = university.id
        if uid not in uni_data:
            uni_data[uid] = {
                "university": university,
                "records": [],
            }
        uni_data[uid]["records"].append((record, major))

    # 3. 对每所院校计算推荐得分
    all_recommendations: list[UniversityRecommendation] = []

    for uid, data in uni_data.items():
        uni = data["university"]
        records = data["records"]

        # 取最近年份最低位次做冲稳保分类
        latest_records = sorted(records, key=lambda r: -r[0].year)
        latest_min_rank = latest_records[0][0].min_rank
        if latest_min_rank is None:
            continue

        tier = classify_by_rank(latest_min_rank, score.rank, rank_ranges)
        if tier is None:
            continue

        # 排除专业
        if score.excluded_majors:
            records = [
                (r, m) for r, m in records
                if m.category not in score.excluded_majors
            ]
            if not records:
                continue

        # 位次匹配得分
        r_score = rank_match_score(latest_min_rank, score.rank)

        # 3年位次列表
        min_ranks_3yr = []
        for r, m in sorted(records, key=lambda x: -x[0].year)[:3]:
            if r.min_rank:
                min_ranks_3yr.append(r.min_rank)

        # 对每个专业计算单科适配
        major_recs = []
        for record, major in records:
            subject_weights = major.subject_weights
            category = major.category or "理工类"

            # 单科适配度
            adapt_score = compute_subject_adapt_score(
                student_scores, subject_weights, category,
            )

            # 逐科匹配详情
            avg_scores = {}
            min_scores = {}
            for subj in ["语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理"]:
                attr_avg = f"avg_{_subject_to_field(subj)}"
                attr_min = f"min_{_subject_to_field(subj)}"
                if hasattr(record, attr_avg):
                    val = getattr(record, attr_avg)
                    if val is not None:
                        avg_scores[subj] = val
                if hasattr(record, attr_min):
                    val = getattr(record, attr_min)
                    if val is not None:
                        min_scores[subj] = val

            match_details = generate_subject_match_details(
                student_scores, avg_scores, min_scores, subject_weights,
            )

            # 标签 & 风险
            adapt_tags, risk_notes = generate_adapt_tags(
                student_scores, subject_weights, category,
            )

            # 最低分检查
            min_warnings = check_subject_minimums(
                student_scores, major.min_subject_scores,
            )
            risk_notes.extend(min_warnings)

            major_recs.append(MajorRecommendation(
                major_id=major.id,
                major_name=major.name,
                category=major.category or "",
                subject_match_details=match_details,
                subject_adapt_score=adapt_score,
                adapt_tags=adapt_tags,
                risk_notes=risk_notes,
            ))

        if not major_recs:
            continue

        # 院校级单科适配度 = 所有专业适配度的加权平均
        avg_adapt = sum(m.subject_adapt_score for m in major_recs) / len(major_recs)

        # 综合得分
        total = r_score * RANK_WEIGHT + avg_adapt * SUBJECT_WEIGHT

        # 风险等级
        risk_level = "low"
        all_risks = []
        for mr in major_recs:
            all_risks.extend(mr.risk_notes)
        if len(all_risks) > 3:
            risk_level = "high"
        elif len(all_risks) > 0:
            risk_level = "medium"

        # 院校标签
        tags = []
        if uni.level:
            tags.append(uni.level)
        if uni.type:
            tags.append(uni.type)

        # 按适配度排序专业，取top
        major_recs.sort(key=lambda m: -m.subject_adapt_score)

        all_recommendations.append(UniversityRecommendation(
            university_id=uid,
            university_name=uni.name,
            province=uni.province or "",
            city=uni.city or "",
            level=uni.level or "",
            is_public=uni.is_public or True,
            tier=tier,
            rank_match_score=round(r_score, 2),
            min_rank_3yr=min_ranks_3yr,
            subject_adapt_score=round(avg_adapt, 2),
            total_score=round(total, 2),
            recommended_majors=major_recs[:5],
            tags=tags,
            risk_level=risk_level,
        ))

    # 4. 按 tier 分组 & 排序
    rush = sorted(
        [r for r in all_recommendations if r.tier == "rush"],
        key=lambda x: -x.total_score,
    )[:request.limit]
    stable = sorted(
        [r for r in all_recommendations if r.tier == "stable"],
        key=lambda x: -x.total_score,
    )[:request.limit]
    safe = sorted(
        [r for r in all_recommendations if r.tier == "safe"],
        key=lambda x: -x.total_score,
    )[:request.limit]

    # 策略调整
    if request.strategy == "rush_first":
        rush = rush[:request.limit * 2]
        stable = stable[:request.limit // 2]
        safe = safe[:request.limit // 2]
    elif request.strategy == "safe_first":
        safe = safe[:request.limit * 2]
        stable = stable[:request.limit // 2]
        rush = rush[:request.limit // 2]
    elif request.strategy == "major_fit":
        # 按单科适配度排序优先
        for group in [rush, stable, safe]:
            group.sort(key=lambda x: -x.subject_adapt_score)

    summary = {
        "total_count": len(all_recommendations),
        "rush_count": len(rush),
        "stable_count": len(stable),
        "safe_count": len(safe),
        "student_rank": score.rank,
        "student_total_score": score.total_score,
        "province": score.province,
    }

    return RecommendResult(rush=rush, stable=stable, safe=safe, summary=summary)


def _subject_to_field(subj: str) -> str:
    """中文科目名 -> 数据库字段名"""
    mapping = {
        "语文": "chinese",
        "数学": "math",
        "英语": "english",
        "物理": "physics",
        "化学": "chemistry",
        "生物": "biology",
        "政治": "politics",
        "历史": "history",
        "地理": "geography",
    }
    return mapping.get(subj, subj)
