"""借用Schema"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class BorrowBase(BaseModel):
    asset_id: int
    reason: Optional[str] = None
    expected_return_date: Optional[date] = None


class BorrowCreate(BorrowBase):
    pass


class BorrowUpdate(BaseModel):
    status: Optional[str] = None
    actual_return_date: Optional[date] = None


class BorrowApprove(BaseModel):
    approve: bool
    comment: Optional[str] = None


class BorrowResponse(BorrowBase):
    id: int
    user_id: int
    approver_id: Optional[int] = None
    status: str
    actual_return_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
