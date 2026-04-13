# 资产分类数据库模型
from typing import Optional, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin


class Category(Base, TimestampMixin):
    """资产分类模型"""
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="分类描述")
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="图标名称")

    # 关联关系
    assets: Mapped[List["Asset"]] = relationship("Asset", back_populates="category")
