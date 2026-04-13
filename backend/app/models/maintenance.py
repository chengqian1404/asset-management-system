# 维修记录数据库模型
from datetime import date
from typing import Optional
from decimal import Decimal
from sqlalchemy import String, Date, Numeric, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class MaintenanceRecord(Base):
    """资产维修记录模型"""
    __tablename__ = "maintenance_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False, comment="资产ID")
    maintenance_date: Mapped[date] = mapped_column(Date, nullable=False, comment="维修日期")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="维修描述")
    cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="维修费用")
    maintained_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="维修人员")
    created_at: Mapped[date] = mapped_column(Date, nullable=False, comment="记录创建时间")

    # 关联关系
    asset: Mapped["Asset"] = relationship("Asset", back_populates="maintenance_records")
