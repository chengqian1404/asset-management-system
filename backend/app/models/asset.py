"""资产模型"""
from sqlalchemy import Column, Integer, String, Text, Date, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
from .base import TimestampMixin


class Asset(Base, TimestampMixin):
    """资产表"""
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_number = Column(String(50), unique=True, nullable=False, index=True, comment="资产编号")
    name = Column(String(200), nullable=False, comment="资产名称")
    category_id = Column(Integer, ForeignKey("categories.id"), comment="分类ID")
    status = Column(String(20), default="idle", comment="状态")
    location = Column(String(200), comment="存放位置")
    owner_id = Column(Integer, ForeignKey("users.id"), comment="负责人ID")
    purchase_date = Column(Date, comment="购置日期")
    purchase_price = Column(Numeric(12, 2), comment="购置金额")
    supplier = Column(String(200), comment="供应商")
    description = Column(Text, comment="描述")
    qr_code = Column(Text, comment="二维码数据")

    # 关联关系
    category = relationship("Category", back_populates="assets")
    owner = relationship("User", back_populates="assets", foreign_keys=[owner_id])
    borrows = relationship("Borrow", back_populates="asset")
