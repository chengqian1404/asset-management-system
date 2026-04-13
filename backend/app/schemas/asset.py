# 资产相关Schema定义
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.constants.status import AssetStatus
from app.schemas.category import CategoryResponse
from app.schemas.user import UserResponse


class AssetBase(BaseModel):
    """资产基础字段"""
    asset_number: str
    name: str
    category_id: Optional[int] = None
    status: AssetStatus = AssetStatus.IDLE
    location: Optional[str] = None
    owner_id: Optional[int] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[Decimal] = None
    supplier: Optional[str] = None
    description: Optional[str] = None


class AssetCreate(AssetBase):
    """创建资产请求"""
    pass


class AssetUpdate(BaseModel):
    """更新资产请求"""
    name: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[AssetStatus] = None
    location: Optional[str] = None
    owner_id: Optional[int] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[Decimal] = None
    supplier: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class AssetResponse(AssetBase):
    """资产响应数据"""
    id: int
    qr_code: Optional[str] = None
    category: Optional[CategoryResponse] = None
    owner: Optional[UserResponse] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssetStats(BaseModel):
    """资产统计数据"""
    total: int = 0          # 总数
    in_use: int = 0         # 在用数量
    idle: int = 0           # 闲置数量
    maintenance: int = 0    # 维修中数量
    scrapped: int = 0       # 已报废数量
    borrowed: int = 0       # 已借出数量


class AssetImportRow(BaseModel):
    """资产导入行数据"""
    asset_number: str
    name: str
    category_name: Optional[str] = None
    location: Optional[str] = None
    purchase_date: Optional[str] = None
    purchase_price: Optional[str] = None
    supplier: Optional[str] = None
    description: Optional[str] = None
