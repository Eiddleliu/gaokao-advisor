from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./gaokao.db"
    DEBUG: bool = True
    # 推荐算法参数（可调节）
    RUSH_RATIO_MIN: float = 0.85   # 冲刺：位次下限系数
    RUSH_RATIO_MAX: float = 0.95   # 冲刺：位次上限系数
    STABLE_RATIO_MIN: float = 0.98 # 稳妥：位次下限系数
    STABLE_RATIO_MAX: float = 1.10 # 稳妥：位次上限系数
    SAFE_RATIO_MIN: float = 1.20   # 保底：位次下限系数
    SAFE_RATIO_MAX: float = 1.40   # 保底：位次上限系数


settings = Settings()
