"""认证API端点"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest, RegisterRequest
from ..schemas.user import UserResponse
from ..services.auth_service import AuthService
from ..api.deps import get_current_user
from ..models.user import User

router = APIRouter()


@router.post("/login", response_model=TokenResponse, summary="用户登录")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """用户登录，返回JWT Token"""
    service = AuthService(db)
    return service.login(request.username, request.password)


@router.post("/refresh", response_model=TokenResponse, summary="刷新Token")
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """刷新访问Token"""
    service = AuthService(db)
    return service.refresh_token(request.refresh_token)


@router.post("/register", response_model=UserResponse, summary="用户注册")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """注册新用户"""
    service = AuthService(db)
    return service.register(request)


@router.get("/me", response_model=UserResponse, summary="获取当前用户")
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return current_user
