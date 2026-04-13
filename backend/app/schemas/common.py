# 通用响应Schema定义
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class SuccessResponse(BaseModel):
    """标准成功响应格式"""
    code: int = 200
    message: str = "成功"
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """标准错误响应格式"""
    code: int
    message: str
    detail: Optional[str] = None


class PaginationResponse(BaseModel, Generic[T]):
    """分页响应格式"""
    total: int
    page: int
    page_size: int
    items: List[T]


class PaginationParams(BaseModel):
    """分页请求参数"""
    page: int = 1
    page_size: int = 20

    model_config = ConfigDict(extra="ignore")
