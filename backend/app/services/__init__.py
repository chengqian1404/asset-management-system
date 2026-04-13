# 服务模块初始化
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.asset_service import AssetService
from app.services.borrow_service import BorrowService
from app.services.report_service import ReportService
from app.services.operation_log_service import OperationLogService

__all__ = [
    "AuthService",
    "UserService",
    "AssetService",
    "BorrowService",
    "ReportService",
    "OperationLogService",
]
