"""操作日志模型"""
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class OperationLog(Base):
    """操作日志表"""
    __tablename__ = "operation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), comment="操作人ID")
    action = Column(String(100), nullable=False, comment="操作类型")
    table_name = Column(String(50), comment="操作表名")
    record_id = Column(Integer, comment="记录ID")
    old_values = Column(JSON, comment="修改前数据")
    new_values = Column(JSON, comment="修改后数据")
    ip_address = Column(String(50), comment="IP地址")
    created_at = Column(DateTime, server_default=func.now())

    # 关联关系
    user = relationship("User", back_populates="operation_logs")
