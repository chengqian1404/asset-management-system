# 模型模块初始化，导入所有模型确保Alembic能够发现
from app.models.base import Base, TimestampMixin
from app.models.user import User
from app.models.category import Category
from app.models.asset import Asset
from app.models.borrow import Borrow
from app.models.maintenance import MaintenanceRecord
from app.models.asset_transfer import AssetTransfer
from app.models.operation_log import OperationLog
from app.models.system_setting import SystemSetting

__all__ = [
    "Base",
    "TimestampMixin",
    "User",
    "Category",
    "Asset",
    "Borrow",
    "MaintenanceRecord",
    "AssetTransfer",
    "OperationLog",
    "SystemSetting",
]
