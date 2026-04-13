# 借用相关Schema定义
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.constants.borrow_status import BorrowStatus
from app.schemas.asset import AssetResponse
from app.schemas.user import UserResponse


class BorrowBase(BaseModel):
    """借用基础字段"""
    asset_id: int
    reason: Optional[str] = None
    expected_return_date: Optional[date] = None


class BorrowCreate(BorrowBase):
    """创建借用申请请求"""
    pass


class BorrowApprove(BaseModel):
    """审批借用请求"""
    comment: Optional[str] = None  # 审批意见


class BorrowReject(BaseModel):
    """拒绝借用请求"""
    comment: Optional[str] = None  # 拒绝原因


class BorrowReturn(BaseModel):
    """归还资产请求"""
    comment: Optional[str] = None  # 归还备注


class BorrowResponse(BorrowBase):
    """借用记录响应数据"""
    id: int
    user_id: int
    approver_id: Optional[int] = None
    status: BorrowStatus
    actual_return_date: Optional[date] = None
    asset: Optional[AssetResponse] = None
    user: Optional[UserResponse] = None
    approver: Optional[UserResponse] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
