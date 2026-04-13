# 借用管理API路由
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.common import SuccessResponse, PaginationResponse
from app.schemas.borrow import BorrowCreate, BorrowApprove, BorrowReject, BorrowReturn, BorrowResponse
from app.services.borrow_service import BorrowService
from app.services.operation_log_service import OperationLogService
from app.api.deps import get_current_active_user, require_admin_or_approver
from app.models.user import User

router = APIRouter(prefix="/borrows", tags=["借用管理"])


@router.get("", response_model=SuccessResponse, summary="获取借用记录列表")
def get_borrows(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="借用状态筛选"),
    asset_id: Optional[int] = Query(None, description="资产ID筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_approver),
):
    """获取所有借用记录（管理员或审批人）"""
    total, borrows = BorrowService.get_borrows(db, page, page_size, status, None, asset_id)
    items = [BorrowResponse.model_validate(b).model_dump() for b in borrows]
    return SuccessResponse(
        data=PaginationResponse(total=total, page=page, page_size=page_size, items=items)
    )


@router.get("/my", response_model=SuccessResponse, summary="获取我的借用记录")
def get_my_borrows(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="借用状态筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取当前用户的借用记录"""
    total, borrows = BorrowService.get_borrows(db, page, page_size, status, current_user.id)
    items = [BorrowResponse.model_validate(b).model_dump() for b in borrows]
    return SuccessResponse(
        data=PaginationResponse(total=total, page=page, page_size=page_size, items=items)
    )


@router.post("", response_model=SuccessResponse, summary="申请借用")
def create_borrow(
    borrow_data: BorrowCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """提交借用申请"""
    borrow = BorrowService.create_borrow(db, borrow_data, current_user.id)
    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="create_borrow", user_id=current_user.id,
        table_name="borrows", record_id=borrow.id,
        new_values={"asset_id": borrow.asset_id, "reason": borrow.reason},
        ip_address=ip,
    )
    db.commit()
    return SuccessResponse(message="借用申请提交成功", data=BorrowResponse.model_validate(borrow).model_dump())


@router.get("/{borrow_id}", response_model=SuccessResponse, summary="获取借用详情")
def get_borrow(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取指定借用记录详情"""
    borrow = BorrowService.get_borrow(db, borrow_id)
    # 普通用户只能查看自己的借用记录
    from app.constants.role import UserRole
    if current_user.role == UserRole.USER and borrow.user_id != current_user.id:
        from app.utils.exceptions import PermissionError
        raise PermissionError("只能查看自己的借用记录")
    return SuccessResponse(data=BorrowResponse.model_validate(borrow).model_dump())


@router.put("/{borrow_id}/approve", response_model=SuccessResponse, summary="审批通过")
def approve_borrow(
    borrow_id: int,
    approve_data: BorrowApprove,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_approver),
):
    """审批通过借用申请（管理员或审批人）"""
    borrow = BorrowService.approve_borrow(db, borrow_id, current_user.id)
    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="approve_borrow", user_id=current_user.id,
        table_name="borrows", record_id=borrow_id,
        new_values={"status": "approved", "comment": approve_data.comment},
        ip_address=ip,
    )
    db.commit()
    return SuccessResponse(message="借用申请已批准", data=BorrowResponse.model_validate(borrow).model_dump())


@router.put("/{borrow_id}/reject", response_model=SuccessResponse, summary="拒绝借用")
def reject_borrow(
    borrow_id: int,
    reject_data: BorrowReject,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_approver),
):
    """拒绝借用申请（管理员或审批人）"""
    borrow = BorrowService.reject_borrow(db, borrow_id, current_user.id)
    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="reject_borrow", user_id=current_user.id,
        table_name="borrows", record_id=borrow_id,
        new_values={"status": "rejected", "comment": reject_data.comment},
        ip_address=ip,
    )
    db.commit()
    return SuccessResponse(message="借用申请已拒绝", data=BorrowResponse.model_validate(borrow).model_dump())


@router.put("/{borrow_id}/return", response_model=SuccessResponse, summary="归还资产")
def return_asset(
    borrow_id: int,
    return_data: BorrowReturn,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """处理资产归还"""
    borrow = BorrowService.return_asset(db, borrow_id, current_user.id, current_user.role)
    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="return_asset", user_id=current_user.id,
        table_name="borrows", record_id=borrow_id,
        new_values={"status": "returned", "actual_return_date": str(borrow.actual_return_date)},
        ip_address=ip,
    )
    db.commit()
    return SuccessResponse(message="资产归还成功", data=BorrowResponse.model_validate(borrow).model_dump())
