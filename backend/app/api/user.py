"""用户管理API端点"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from ..schemas.user import UserCreate, UserUpdate, UserResponse
from ..services.user_service import UserService
from ..api.deps import get_current_user, get_admin_user
from ..models.user import User

router = APIRouter()


@router.get("", summary="获取用户列表")
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """获取用户列表（需要管理员权限）"""
    service = UserService(db)
    return service.list_users(page, page_size, keyword)


@router.post("", response_model=UserResponse, summary="新增用户")
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """新增用户（需要管理员权限）"""
    service = UserService(db)
    return service.create_user(user)


@router.put("/{user_id}", response_model=UserResponse, summary="修改用户")
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """修改用户信息（需要管理员权限）"""
    service = UserService(db)
    return service.update_user(user_id, user)


@router.delete("/{user_id}", summary="删除用户")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """删除用户（需要管理员权限）"""
    service = UserService(db)
    service.delete_user(user_id)
    return {"message": "删除成功"}
