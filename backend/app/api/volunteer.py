"""志愿规划 API"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.models import VolunteerPlan, University, Major, AdmissionRecord

router = APIRouter()


class VolunteerChoiceItem(BaseModel):
    university_id: int
    university_name: str
    major_id: int
    major_name: str
    tier: str  # 冲刺/稳妥/保底
    order: int
    is_adjust: bool = True


class CreatePlanRequest(BaseModel):
    user_id: int
    score_id: int
    name: str
    strategy: str
    choices: list[VolunteerChoiceItem]


class PlanResponse(BaseModel):
    id: int
    name: str
    strategy: str
    choices: list
    risk_notes: list
    created_at: str


@router.post("/plan", summary="创建志愿方案")
async def create_plan(req: CreatePlanRequest, db: AsyncSession = Depends(get_db)):
    """保存一套志愿方案"""
    choices_data = [c.model_dump() for c in req.choices]

    # 风险检测
    risk_notes = await _detect_risks(db, req.choices)

    plan = VolunteerPlan(
        user_id=req.user_id,
        score_id=req.score_id,
        name=req.name,
        strategy=req.strategy,
        choices=choices_data,
        risk_notes=risk_notes,
    )
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return {"id": plan.id, "name": plan.name, "risk_notes": risk_notes}


@router.get("/plans/{user_id}", summary="用户的志愿方案列表")
async def list_plans(user_id: int, db: AsyncSession = Depends(get_db)):
    """获取用户所有志愿方案"""
    stmt = select(VolunteerPlan).where(VolunteerPlan.user_id == user_id)
    result = await db.execute(stmt)
    plans = result.scalars().all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "strategy": p.strategy,
            "choice_count": len(p.choices) if p.choices else 0,
            "risk_count": len(p.risk_notes) if p.risk_notes else 0,
            "created_at": str(p.created_at),
        }
        for p in plans
    ]


@router.get("/plan/{plan_id}", summary="方案详情")
async def get_plan(plan_id: int, db: AsyncSession = Depends(get_db)):
    """获取方案详情"""
    result = await db.execute(select(VolunteerPlan).where(VolunteerPlan.id == plan_id))
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(404, "方案不存在")
    return {
        "id": plan.id,
        "name": plan.name,
        "strategy": plan.strategy,
        "choices": plan.choices,
        "risk_notes": plan.risk_notes,
    }


@router.post("/risk-check", summary="志愿风险检测")
async def risk_check(choices: list[VolunteerChoiceItem], db: AsyncSession = Depends(get_db)):
    """对一组志愿选项做风险检测"""
    risks = await _detect_risks(db, choices)
    return {"risk_count": len(risks), "risks": risks}


async def _detect_risks(db: AsyncSession, choices: list[VolunteerChoiceItem]) -> list[dict]:
    """
    风险检测逻辑：
    1. 滑档风险：未勾选服从调剂
    2. 梯度风险：冲刺占比过高
    3. 重复风险：同一院校出现多次
    """
    risks = []
    uni_ids = []

    for c in choices:
        # 调剂风险
        if not c.is_adjust:
            risks.append({
                "type": "adjust_risk",
                "level": "high",
                "message": f"【{c.university_name}-{c.major_name}】未勾选服从调剂，存在滑档风险",
                "university_id": c.university_id,
            })

        # 重复检测
        if c.university_id in uni_ids:
            risks.append({
                "type": "duplicate",
                "level": "medium",
                "message": f"【{c.university_name}】在志愿表中重复出现",
                "university_id": c.university_id,
            })
        uni_ids.append(c.university_id)

    # 梯度检测
    rush_count = sum(1 for c in choices if c.tier == "冲刺")
    total = len(choices)
    if total > 0 and rush_count / total > 0.5:
        risks.append({
            "type": "gradient_risk",
            "level": "high",
            "message": f"冲刺院校占比 {rush_count}/{total}（超过50%），整体风险偏高，建议增加稳妥和保底院校",
        })

    # 保底检测
    safe_count = sum(1 for c in choices if c.tier == "保底")
    if total > 0 and safe_count == 0:
        risks.append({
            "type": "no_safe",
            "level": "medium",
            "message": "未设置保底院校，存在全部滑档的极端风险",
        })

    return risks
