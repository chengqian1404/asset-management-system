# 分类相关Schema定义
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    """分类基础字段"""
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None


class CategoryCreate(CategoryBase):
    """创建分类请求"""
    pass


class CategoryUpdate(BaseModel):
    """更新分类请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class CategoryResponse(CategoryBase):
    """分类响应数据"""
    id: int
    asset_count: Optional[int] = 0   # 该分类下的资产数量
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
