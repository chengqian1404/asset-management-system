"""报表API端点"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.report_service import ReportService
from ..api.deps import get_current_user
from ..models.user import User

router = APIRouter()


@router.get("/asset-stats", summary="资产统计")
async def asset_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取资产统计报表"""
    service = ReportService(db)
    return service.asset_stats()


@router.get("/borrow-stats", summary="借用统计")
async def borrow_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取借用统计报表"""
    service = ReportService(db)
    return service.borrow_stats()


@router.get("/category-stats", summary="分类统计")
async def category_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取按分类的资产统计"""
    service = ReportService(db)
    return service.category_stats()
