"""通用Schema"""
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, List, Any

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    """统一响应模型"""
    code: int = 200
    message: str = "成功"
    data: Optional[T] = None


class PageInfo(BaseModel):
    """分页信息"""
    total: int
    page: int
    page_size: int
    total_pages: int


class PagedResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    code: int = 200
    message: str = "成功"
    data: Optional[List[T]] = None
    page_info: Optional[PageInfo] = None
