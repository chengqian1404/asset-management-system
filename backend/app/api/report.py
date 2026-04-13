# 报告API路由
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.common import SuccessResponse
from app.services.report_service import ReportService
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["统计报告"])


@router.get("/asset-stats", response_model=SuccessResponse, summary="资产统计报告")
def get_asset_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取资产统计报告：按状态、分类统计及近期新增"""
    stats = ReportService.get_asset_stats(db)
    return SuccessResponse(data=stats.model_dump())


@router.get("/borrow-stats", response_model=SuccessResponse, summary="借用统计报告")
def get_borrow_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取借用统计报告：按状态统计及月度趋势"""
    stats = ReportService.get_borrow_stats(db)
    return SuccessResponse(data=stats.model_dump())


@router.get("/category-stats", response_model=SuccessResponse, summary="分类统计报告")
def get_category_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取各分类资产数量统计报告"""
    stats = ReportService.get_category_stats(db)
    return SuccessResponse(data=stats.model_dump())
