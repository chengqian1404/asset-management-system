# 用户数据库模型
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin
from app.constants.role import UserRole


class User(Base, TimestampMixin):
    """用户模型"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码哈希")
    full_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="姓名")
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="部门")
    role: Mapped[str] = mapped_column(
        SAEnum(UserRole, values_callable=lambda x: [e.value for e in x]),
        default=UserRole.USER,
        nullable=False,
        comment="用户角色"
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="是否激活")
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="最后登录时间")

    # 关联关系
    owned_assets: Mapped[List["Asset"]] = relationship("Asset", back_populates="owner", foreign_keys="Asset.owner_id")
    borrow_records: Mapped[List["Borrow"]] = relationship("Borrow", back_populates="user", foreign_keys="Borrow.user_id")
    approved_borrows: Mapped[List["Borrow"]] = relationship("Borrow", back_populates="approver", foreign_keys="Borrow.approver_id")
    operation_logs: Mapped[List["OperationLog"]] = relationship("OperationLog", back_populates="user")
    transfers_from: Mapped[List["AssetTransfer"]] = relationship("AssetTransfer", back_populates="from_user", foreign_keys="AssetTransfer.from_user_id")
    transfers_to: Mapped[List["AssetTransfer"]] = relationship("AssetTransfer", back_populates="to_user", foreign_keys="AssetTransfer.to_user_id")
