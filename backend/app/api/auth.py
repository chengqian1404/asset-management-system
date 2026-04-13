# 认证API路由
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest
from app.schemas.common import SuccessResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.services.operation_log_service import OperationLogService
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=SuccessResponse, summary="用户登录")
def login(
    login_data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """用户登录，返回JWT访问令牌和刷新令牌"""
    user, token_response = AuthService.login(db, login_data)

    # 记录登录日志
    ip_address = request.client.host if request.client else None
    OperationLogService.log(
        db=db,
        action="login",
        user_id=user.id,
        table_name="users",
        record_id=user.id,
        new_values={"username": user.username},
        ip_address=ip_address,
    )
    db.commit()

    return SuccessResponse(
        message="登录成功",
        data={
            "user": UserResponse.model_validate(user).model_dump(),
            "token": token_response.model_dump(),
        }
    )


@router.post("/refresh", response_model=SuccessResponse, summary="刷新令牌")
def refresh_token(
    refresh_data: RefreshTokenRequest,
):
    """使用刷新令牌获取新的访问令牌"""
    token_response = AuthService.refresh_token(refresh_data.refresh_token)
    return SuccessResponse(message="令牌刷新成功", data=token_response.model_dump())


@router.get("/me", response_model=SuccessResponse, summary="获取当前用户信息")
def get_me(current_user: User = Depends(get_current_active_user)):
    """获取当前登录用户的详细信息"""
    return SuccessResponse(
        message="获取成功",
        data=UserResponse.model_validate(current_user).model_dump()
    )


@router.post("/logout", response_model=SuccessResponse, summary="退出登录")
def logout(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """退出登录（客户端应清除存储的令牌）"""
    ip_address = request.client.host if request.client else None
    OperationLogService.log(
        db=db,
        action="logout",
        user_id=current_user.id,
        table_name="users",
        record_id=current_user.id,
        ip_address=ip_address,
    )
    db.commit()

    return SuccessResponse(message="退出登录成功")
