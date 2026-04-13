"""用户模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
from .base import TimestampMixin


class User(Base, TimestampMixin):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True, comment="用户名")
    email = Column(String(100), unique=True, nullable=False, comment="邮箱")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    full_name = Column(String(100), comment="姓名")
    department = Column(String(100), comment="部门")
    role = Column(String(20), default="user", comment="角色")
    is_active = Column(Boolean, default=True, comment="是否启用")

    # 关联关系
    assets = relationship("Asset", back_populates="owner", foreign_keys="Asset.owner_id")
    borrows = relationship("Borrow", back_populates="user", foreign_keys="Borrow.user_id")
    approved_borrows = relationship("Borrow", back_populates="approver", foreign_keys="Borrow.approver_id")
    operation_logs = relationship("OperationLog", back_populates="user")
