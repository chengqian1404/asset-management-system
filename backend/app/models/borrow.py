# 借用记录数据库模型
from datetime import date
from typing import Optional
from sqlalchemy import String, Date, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin
from app.constants.borrow_status import BorrowStatus


class Borrow(Base, TimestampMixin):
    """借用记录模型"""
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False, comment="资产ID")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, comment="申请人ID")
    approver_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, comment="审批人ID")
    status: Mapped[str] = mapped_column(
        SAEnum(BorrowStatus, values_callable=lambda x: [e.value for e in x]),
        default=BorrowStatus.PENDING,
        nullable=False,
        comment="借用状态"
    )
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="借用原因")
    expected_return_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="预计归还日期")
    actual_return_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="实际归还日期")

    # 关联关系
    asset: Mapped["Asset"] = relationship("Asset", back_populates="borrow_records")
    user: Mapped["User"] = relationship("User", back_populates="borrow_records", foreign_keys=[user_id])
    approver: Mapped[Optional["User"]] = relationship("User", back_populates="approved_borrows", foreign_keys=[approver_id])
