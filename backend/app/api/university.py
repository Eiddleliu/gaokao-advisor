"""院校 & 专业查询 API"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import University, Major, AdmissionRecord
from app.schemas.university import UniversityDetail, MajorDetail

router = APIRouter()


@router.get("/list", summary="院校列表查询")
async def list_universities(
    keyword: str = Query(None, description="关键词搜索"),
    province: str = Query(None),
    city: str = Query(None),
    level: str = Query(None, description="985/211/双一流/公办本科/民办本科"),
    type_: str = Query(None, alias="type", description="综合/理工/师范/医药等"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """分页查询院校列表，支持关键词、省份、层次等筛选"""
    stmt = select(University)

    if keyword:
        stmt = stmt.where(University.name.contains(keyword))
    if province:
        stmt = stmt.where(University.province == province)
    if city:
        stmt = stmt.where(University.city == city)
    if level:
        stmt = stmt.where(University.level == level)
    if type_:
        stmt = stmt.where(University.type == type_)

    # Count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0

    # Paginate
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    unis = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "id": u.id,
                "name": u.name,
                "province": u.province,
                "city": u.city,
                "level": u.level,
                "type": u.type,
                "is_public": u.is_public,
                "top_majors": u.top_majors,
                "postgraduate_rate": u.postgraduate_rate,
                "employment_rate": u.employment_rate,
            }
            for u in unis
        ],
    }


@router.get("/{university_id}", response_model=UniversityDetail, summary="院校详情")
async def get_university(university_id: int, db: AsyncSession = Depends(get_db)):
    """获取院校详细信息"""
    result = await db.execute(select(University).where(University.id == university_id))
    uni = result.scalar_one_or_none()
    if not uni:
        from fastapi import HTTPException
        raise HTTPException(404, "院校不存在")
    return uni


@router.get("/{university_id}/majors", summary="院校专业列表")
async def list_majors(
    university_id: int,
    category: str = Query(None, description="专业大类"),
    db: AsyncSession = Depends(get_db),
):
    """获取某院校的所有专业"""
    stmt = select(Major).where(Major.university_id == university_id)
    if category:
        stmt = stmt.where(Major.category == category)
    result = await db.execute(stmt)
    majors = result.scalars().all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "category": m.category,
            "duration": m.duration,
            "degree": m.degree,
            "subject_requirement": m.subject_requirement,
            "subject_weights": m.subject_weights,
            "min_subject_scores": m.min_subject_scores,
        }
        for m in majors
    ]


@router.get("/major/{major_id}", response_model=MajorDetail, summary="专业详情")
async def get_major(major_id: int, db: AsyncSession = Depends(get_db)):
    """获取专业详情"""
    result = await db.execute(select(Major).where(Major.id == major_id))
    major = result.scalar_one_or_none()
    if not major:
        from fastapi import HTTPException
        raise HTTPException(404, "专业不存在")
    return major


@router.get("/{university_id}/admissions", summary="院校录取数据")
async def get_admissions(
    university_id: int,
    province: str = Query(...),
    year: int = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取院校某省的历年录取数据（含单科平均分）"""
    stmt = (
        select(AdmissionRecord, Major)
        .join(Major, AdmissionRecord.major_id == Major.id)
        .where(AdmissionRecord.university_id == university_id)
        .where(AdmissionRecord.province == province)
    )
    if year:
        stmt = stmt.where(AdmissionRecord.year == year)
    stmt = stmt.order_by(AdmissionRecord.year.desc())

    result = await db.execute(stmt)
    rows = result.all()

    return [
        {
            "year": r.year,
            "batch": r.batch,
            "major_name": m.name,
            "major_category": m.category,
            "min_total_score": r.min_total_score,
            "avg_total_score": r.avg_total_score,
            "min_rank": r.min_rank,
            "avg_rank": r.avg_rank,
            "subject_avg": {
                "语文": r.avg_chinese, "数学": r.avg_math, "英语": r.avg_english,
                "物理": r.avg_physics, "化学": r.avg_chemistry, "生物": r.avg_biology,
                "政治": r.avg_politics, "历史": r.avg_history, "地理": r.avg_geography,
            },
            "subject_min": {
                "数学": r.min_math, "英语": r.min_english, "物理": r.min_physics,
            },
        }
        for r, m in rows
    ]
