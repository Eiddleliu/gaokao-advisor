"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import recommend, university, volunteer, score
from app.database import engine, Base


def create_app() -> FastAPI:
    application = FastAPI(
        title="高考志愿智能推荐系统",
        description="基于单科分数加权匹配的院校专业推荐平台",
        version="0.1.0",
    )

    # CORS – allow Vue dev server
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    application.include_router(recommend.router, prefix="/api/recommend", tags=["智能推荐"])
    application.include_router(university.router, prefix="/api/university", tags=["院校查询"])
    application.include_router(volunteer.router, prefix="/api/volunteer", tags=["志愿规划"])
    application.include_router(score.router, prefix="/api/score", tags=["分数查询"])

    @application.on_event("startup")
    async def on_startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return application


app = create_app()
