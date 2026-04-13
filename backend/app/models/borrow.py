"""借用模型"""
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
from .base import TimestampMixin


class Borrow(Base, TimestampMixin):
    """借用记录表"""
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, comment="资产ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="借用人ID")
    approver_id = Column(Integer, ForeignKey("users.id"), comment="审批人ID")
    status = Column(String(20), default="pending", comment="状态")
    reason = Column(Text, comment="借用原因")
    expected_return_date = Column(Date, comment="预计归还日期")
    actual_return_date = Column(Date, comment="实际归还日期")

    # 关联关系
    asset = relationship("Asset", back_populates="borrows")
    user = relationship("User", back_populates="borrows", foreign_keys=[user_id])
    approver = relationship("User", back_populates="approved_borrows", foreign_keys=[approver_id])
