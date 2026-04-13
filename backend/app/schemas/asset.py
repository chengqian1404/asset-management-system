"""资产Schema"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class AssetBase(BaseModel):
    asset_number: str
    name: str
    category_id: Optional[int] = None
    status: str = "idle"
    location: Optional[str] = None
    owner_id: Optional[int] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[Decimal] = None
    supplier: Optional[str] = None
    description: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = None
    location: Optional[str] = None
    owner_id: Optional[int] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[Decimal] = None
    supplier: Optional[str] = None
    description: Optional[str] = None


class AssetResponse(AssetBase):
    id: int
    qr_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
