# 报告相关Schema定义
from typing import List, Dict, Any
from pydantic import BaseModel


class AssetStatsReport(BaseModel):
    """资产统计报告"""
    total: int = 0
    by_status: Dict[str, int] = {}      # 按状态统计
    by_category: Dict[str, int] = {}    # 按分类统计
    recent_added: int = 0               # 近30天新增


class BorrowStatsReport(BaseModel):
    """借用统计报告"""
    total: int = 0
    pending: int = 0
    approved: int = 0
    rejected: int = 0
    returned: int = 0
    overdue: int = 0
    monthly_trend: List[Dict[str, Any]] = []   # 月度趋势


class CategoryStatsReport(BaseModel):
    """分类统计报告"""
    categories: List[Dict[str, Any]] = []   # 各分类资产数量统计
