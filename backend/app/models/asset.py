# 资产数据库模型
from datetime import date
from typing import Optional, List
from decimal import Decimal
from sqlalchemy import String, Date, Numeric, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin
from app.constants.status import AssetStatus


class Asset(Base, TimestampMixin):
    """资产模型"""
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    asset_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False, comment="资产编号")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="资产名称")
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True, comment="分类ID")
    status: Mapped[str] = mapped_column(
        SAEnum(AssetStatus, values_callable=lambda x: [e.value for e in x]),
        default=AssetStatus.IDLE,
        nullable=False,
        comment="资产状态"
    )
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="存放位置")
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, comment="负责人ID")
    purchase_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="购买日期")
    purchase_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True, comment="购买价格")
    supplier: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="供应商")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="备注描述")
    qr_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="二维码Base64数据")

    # 关联关系
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="assets")
    owner: Mapped[Optional["User"]] = relationship("User", back_populates="owned_assets", foreign_keys=[owner_id])
    borrow_records: Mapped[List["Borrow"]] = relationship("Borrow", back_populates="asset")
    maintenance_records: Mapped[List["MaintenanceRecord"]] = relationship("MaintenanceRecord", back_populates="asset")
    transfer_records: Mapped[List["AssetTransfer"]] = relationship("AssetTransfer", back_populates="asset")
