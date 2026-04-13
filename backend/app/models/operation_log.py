# 操作日志数据库模型
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Text, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class OperationLog(Base):
    """操作日志模型，记录系统重要操作"""
    __tablename__ = "operation_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, comment="操作用户ID")
    action: Mapped[str] = mapped_column(String(50), nullable=False, comment="操作类型")
    table_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="操作的表名")
    record_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="操作的记录ID")
    old_values: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="操作前的数据(JSON)")
    new_values: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="操作后的数据(JSON)")
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="客户端IP地址")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False, comment="创建时间")

    # 关联关系
    user: Mapped[Optional["User"]] = relationship("User", back_populates="operation_logs")
