# 应用配置模块
import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """应用配置类，支持从环境变量或.env文件读取"""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # 应用基本配置
    APP_NAME: str = "资产管理系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./asset_management.db"

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production-must-be-long-enough"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30       # 访问令牌有效期30分钟
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7          # 刷新令牌有效期7天

    # CORS配置
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # 分页配置
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024    # 最大上传10MB

    # 备份配置
    BACKUP_DIR: str = "backups"

    @property
    def allowed_origins_list(self) -> list:
        """解析允许的跨域来源列表"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


# 全局配置实例
settings = Settings()
