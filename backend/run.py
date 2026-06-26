"""一键初始化数据库并启动服务"""
import asyncio
import uvicorn


async def init_and_run():
    from app.mock_data.generate import seed_database
    await seed_database()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(init_and_run())
