"""应用配置模块"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # 应用基础配置
    APP_NAME: str = "资产管理系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./asset_management.db"

    # 跨域配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # 管理员初始配置
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    ADMIN_EMAIL: str = "admin@example.com"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
