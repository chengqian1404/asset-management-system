# 认证相关Schema定义
from typing import Optional
from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """令牌响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # 访问令牌有效秒数


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求"""
    refresh_token: str


class TokenData(BaseModel):
    """令牌数据（解码后）"""
    user_id: Optional[int] = None
    username: Optional[str] = None
    token_type: Optional[str] = None  # "access" 或 "refresh"

    model_config = ConfigDict(extra="ignore")
