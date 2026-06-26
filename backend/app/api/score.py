"""分数查询 API（一分一段表、批次线、等位分换算）"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import ScoreSegment, BatchLine

router = APIRouter()


@router.get("/segments", summary="一分一段表查询")
async def get_segments(
    province: str = Query(...),
    year: int = Query(...),
    exam_type: str = Query(None, description="物理类/历史类/理科/文科"),
    score_min: int = Query(None, description="最低分筛选"),
    score_max: int = Query(None, description="最高分筛选"),
    db: AsyncSession = Depends(get_db),
):
    """查询一分一段表"""
    stmt = (
        select(ScoreSegment)
        .where(ScoreSegment.province == province, ScoreSegment.year == year)
    )
    if exam_type:
        stmt = stmt.where(ScoreSegment.exam_type == exam_type)
    if score_min is not None:
        stmt = stmt.where(ScoreSegment.score >= score_min)
    if score_max is not None:
        stmt = stmt.where(ScoreSegment.score <= score_max)
    stmt = stmt.order_by(ScoreSegment.score.desc())

    result = await db.execute(stmt)
    segments = result.scalars().all()
    return [
        {
            "score": s.score,
            "count": s.count,
            "cumulative_count": s.cumulative_count,
            "exam_type": s.exam_type,
        }
        for s in segments
    ]


@router.get("/batch-lines", summary="批次分数线查询")
async def get_batch_lines(
    province: str = Query(...),
    year: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """查询某省某年各批次分数线"""
    stmt = (
        select(BatchLine)
        .where(BatchLine.province == province, BatchLine.year == year)
    )
    result = await db.execute(stmt)
    lines = result.scalars().all()
    return [
        {
            "batch": l.batch,
            "score": l.score,
            "exam_type": l.exam_type,
        }
        for l in lines
    ]


@router.get("/equivalent-score", summary="等位分换算")
async def equivalent_score(
    province: str = Query(...),
    year: int = Query(...),
    rank: int = Query(..., description="位次"),
    exam_type: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    根据位次查对应分数（等位分换算）。
    在一分一段表中找累计人数最接近给定位次的分数。
    """
    stmt = (
        select(ScoreSegment)
        .where(ScoreSegment.province == province, ScoreSegment.year == year)
    )
    if exam_type:
        stmt = stmt.where(ScoreSegment.exam_type == exam_type)
    stmt = stmt.order_by(ScoreSegment.score.desc())

    result = await db.execute(stmt)
    segments = result.scalars().all()

    if not segments:
        return {"score": None, "message": "未找到该省该年数据"}

    # 找累计人数最接近 rank 的分数
    best = min(segments, key=lambda s: abs(s.cumulative_count - rank))
    return {
        "rank": rank,
        "equivalent_score": best.score,
        "actual_cumulative": best.cumulative_count,
        "province": province,
        "year": year,
    }
