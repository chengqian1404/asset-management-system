# 资产转移记录数据库模型
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class AssetTransfer(Base):
    """资产转移记录模型"""
    __tablename__ = "asset_transfers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False, comment="资产ID")
    from_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, comment="转出人ID")
    to_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, comment="转入人ID")
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="转移原因")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False, comment="创建时间")

    # 关联关系
    asset: Mapped["Asset"] = relationship("Asset", back_populates="transfer_records")
    from_user: Mapped[Optional["User"]] = relationship("User", back_populates="transfers_from", foreign_keys=[from_user_id])
    to_user: Mapped["User"] = relationship("User", back_populates="transfers_to", foreign_keys=[to_user_id])
