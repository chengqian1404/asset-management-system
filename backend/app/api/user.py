# 用户管理API路由
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.common import SuccessResponse, PaginationResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserPermissions
from app.services.user_service import UserService
from app.services.operation_log_service import OperationLogService
from app.api.deps import get_current_active_user, require_admin
from app.models.user import User
from typing import Optional

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("", response_model=SuccessResponse, summary="获取用户列表")
def get_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    role: Optional[str] = Query(None, description="按角色筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """获取用户列表（仅管理员）"""
    total, users = UserService.get_users(db, page, page_size, search, role)
    items = [UserResponse.model_validate(u).model_dump() for u in users]
    return SuccessResponse(
        data=PaginationResponse(total=total, page=page, page_size=page_size, items=items)
    )


@router.post("", response_model=SuccessResponse, summary="创建用户")
def create_user(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """创建新用户（仅管理员）"""
    user = UserService.create_user(db, user_data)
    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="create_user", user_id=current_user.id,
        table_name="users", record_id=user.id,
        new_values={"username": user.username, "role": user.role},
        ip_address=ip,
    )
    db.commit()
    return SuccessResponse(message="用户创建成功", data=UserResponse.model_validate(user).model_dump())


@router.put("/{user_id}", response_model=SuccessResponse, summary="更新用户")
def update_user(
    user_id: int,
    user_data: UserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """更新用户信息（仅管理员）"""
    old_user = UserService.get_user(db, user_id)
    old_values = UserResponse.model_validate(old_user).model_dump()

    user = UserService.update_user(db, user_id, user_data)
    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="update_user", user_id=current_user.id,
        table_name="users", record_id=user_id,
        old_values=old_values,
        new_values=UserResponse.model_validate(user).model_dump(),
        ip_address=ip,
    )
    db.commit()
    return SuccessResponse(message="用户更新成功", data=UserResponse.model_validate(user).model_dump())


@router.delete("/{user_id}", response_model=SuccessResponse, summary="删除用户")
def delete_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """删除用户（仅管理员）"""
    old_user = UserService.get_user(db, user_id)
    old_values = {"username": old_user.username}

    UserService.delete_user(db, user_id, current_user.id)
    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="delete_user", user_id=current_user.id,
        table_name="users", record_id=user_id,
        old_values=old_values, ip_address=ip,
    )
    db.commit()
    return SuccessResponse(message="用户删除成功")


@router.get("/{user_id}/permissions", response_model=SuccessResponse, summary="获取用户权限")
def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取用户权限（管理员可查看任意用户，普通用户只能查看自己）"""
    from app.constants.role import UserRole
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        from app.utils.exceptions import PermissionError
        raise PermissionError("只能查看自己的权限")

    user = UserService.get_user(db, user_id)
    permissions = UserService.get_permissions(user)
    return SuccessResponse(data=permissions.model_dump())
