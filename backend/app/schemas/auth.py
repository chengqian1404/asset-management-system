"""认证Schema"""
from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """刷新Token请求"""
    refresh_token: str


class RegisterRequest(BaseModel):
    """注册请求"""
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    department: Optional[str] = None
