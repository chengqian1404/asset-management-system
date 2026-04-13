"""分类模型"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Category(Base):
    """资产分类表"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="分类名称")
    description = Column(Text, comment="分类描述")
    icon = Column(String(50), comment="图标")
    created_at = Column(DateTime, server_default=func.now())

    # 关联关系
    assets = relationship("Asset", back_populates="category")
