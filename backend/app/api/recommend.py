"""智能推荐 API"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.student import RecommendRequest
from app.schemas.recommendation import RecommendResult
from app.algorithm.recommender import get_recommendations

router = APIRouter()


@router.post("/generate", response_model=RecommendResult, summary="生成智能推荐方案")
async def generate_recommendation(
    request: RecommendRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    根据考生单科分数 + 位次，生成冲/稳/保三档推荐方案。

    推荐逻辑：
    1. 第一层：按位次梯度筛选候选院校（冲/稳/保）
    2. 第二层：单科加权打分，优先推送适配你单科优势的专业
    """
    result = await get_recommendations(db, request)
    return result


@router.post("/check-subject-risk", summary="单科风险检测")
async def check_subject_risk(
    request: RecommendRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    检测考生单科分数是否存在风险项（低于专业最低要求）。
    """
    from app.algorithm.subject_weight import get_student_subject_map, check_subject_minimums
    from sqlalchemy import select
    from app.models import Major

    score = request.score
    student_scores = get_student_subject_map(score)

    # 查询所有专业的最低分要求
    stmt = select(Major).where(Major.min_subject_scores.isnot(None))
    result = await db.execute(stmt)
    majors = result.scalars().all()

    risks = []
    for major in majors:
        warnings = check_subject_minimums(student_scores, major.min_subject_scores)
        if warnings:
            risks.append({
                "major_id": major.id,
                "major_name": major.name,
                "warnings": warnings,
            })

    return {"risk_count": len(risks), "risks": risks[:50]}
