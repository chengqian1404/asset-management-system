"""基础模型"""
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class TimestampMixin:
    """时间戳混入类"""
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
