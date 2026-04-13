# Schema模块初始化
from app.schemas.common import SuccessResponse, ErrorResponse, PaginationResponse, PaginationParams
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest, TokenData
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserPermissions
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse, AssetStats
from app.schemas.borrow import BorrowCreate, BorrowApprove, BorrowReject, BorrowReturn, BorrowResponse
from app.schemas.report import AssetStatsReport, BorrowStatsReport, CategoryStatsReport

__all__ = [
    "SuccessResponse", "ErrorResponse", "PaginationResponse", "PaginationParams",
    "LoginRequest", "TokenResponse", "RefreshTokenRequest", "TokenData",
    "UserCreate", "UserUpdate", "UserResponse", "UserPermissions",
    "CategoryCreate", "CategoryUpdate", "CategoryResponse",
    "AssetCreate", "AssetUpdate", "AssetResponse", "AssetStats",
    "BorrowCreate", "BorrowApprove", "BorrowReject", "BorrowReturn", "BorrowResponse",
    "AssetStatsReport", "BorrowStatsReport", "CategoryStatsReport",
]
