# API依赖注入模块
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth_service import AuthService
from app.constants.role import UserRole
from app.utils.exceptions import AuthenticationError, PermissionError

# Bearer令牌安全方案
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """获取当前认证用户的依赖函数"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "未提供认证令牌", "detail": None},
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return AuthService.get_current_user(db, credentials.credentials)
    except AuthenticationError as e:
        raise e


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """确保当前用户是激活状态"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "账号已禁用", "detail": None},
        )
    return current_user


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """要求管理员权限的依赖函数"""
    if current_user.role != UserRole.ADMIN:
        raise PermissionError("此操作需要管理员权限")
    return current_user


def require_admin_or_approver(current_user: User = Depends(get_current_active_user)) -> User:
    """要求管理员或审批人权限的依赖函数"""
    if current_user.role not in [UserRole.ADMIN, UserRole.APPROVER]:
        raise PermissionError("此操作需要管理员或审批人权限")
    return current_user
