"""借用管理API端点"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..schemas.borrow import BorrowCreate, BorrowApprove, BorrowResponse
from ..services.borrow_service import BorrowService
from ..api.deps import get_current_user, get_manager_or_admin
from ..models.user import User

router = APIRouter()


@router.get("", summary="获取借用列表")
async def list_borrows(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取借用记录列表"""
    service = BorrowService(db)
    return service.list_borrows(page, page_size, status, current_user)


@router.get("/my", summary="我的借用记录")
async def my_borrows(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的借用记录"""
    service = BorrowService(db)
    return service.my_borrows(page, page_size, current_user)


@router.post("", response_model=BorrowResponse, summary="申请借用")
async def create_borrow(
    borrow: BorrowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """提交借用申请"""
    service = BorrowService(db)
    return service.create_borrow(borrow, current_user)


@router.put("/{borrow_id}/approve", response_model=BorrowResponse, summary="审批借用")
async def approve_borrow(
    borrow_id: int,
    approve: BorrowApprove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_manager_or_admin)
):
    """审批借用申请"""
    service = BorrowService(db)
    return service.approve_borrow(borrow_id, approve, current_user)


@router.put("/{borrow_id}/return", response_model=BorrowResponse, summary="归还资产")
async def return_borrow(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """归还借用的资产"""
    service = BorrowService(db)
    return service.return_asset(borrow_id, current_user)
