# 报告服务模块
from typing import List, Dict, Any
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.asset import Asset
from app.models.borrow import Borrow
from app.models.category import Category
from app.constants.status import AssetStatus
from app.constants.borrow_status import BorrowStatus
from app.schemas.report import AssetStatsReport, BorrowStatsReport, CategoryStatsReport


class ReportService:
    """报告服务类"""

    @staticmethod
    def get_asset_stats(db: Session) -> AssetStatsReport:
        """获取资产统计报告"""
        total = db.query(Asset).count()

        # 按状态统计
        by_status = {}
        status_counts = db.query(Asset.status, func.count(Asset.id)).group_by(Asset.status).all()
        for status, count in status_counts:
            by_status[status] = count

        # 按分类统计
        by_category = {}
        category_counts = db.query(
            Category.name, func.count(Asset.id)
        ).outerjoin(Asset, Asset.category_id == Category.id) \
         .group_by(Category.name).all()
        for cat_name, count in category_counts:
            if cat_name:
                by_category[cat_name] = count

        # 近30天新增
        thirty_days_ago = date.today() - timedelta(days=30)
        recent_added = db.query(Asset).filter(Asset.created_at >= thirty_days_ago).count()

        return AssetStatsReport(
            total=total,
            by_status=by_status,
            by_category=by_category,
            recent_added=recent_added,
        )

    @staticmethod
    def get_borrow_stats(db: Session) -> BorrowStatsReport:
        """获取借用统计报告"""
        total = db.query(Borrow).count()
        pending = db.query(Borrow).filter(Borrow.status == BorrowStatus.PENDING).count()
        approved = db.query(Borrow).filter(Borrow.status == BorrowStatus.APPROVED).count()
        rejected = db.query(Borrow).filter(Borrow.status == BorrowStatus.REJECTED).count()
        returned = db.query(Borrow).filter(Borrow.status == BorrowStatus.RETURNED).count()
        overdue = db.query(Borrow).filter(Borrow.status == BorrowStatus.OVERDUE).count()

        # 近6个月月度趋势
        monthly_trend = []
        today = date.today()
        for i in range(5, -1, -1):
            # 计算月份
            month_date = date(today.year, today.month, 1) - timedelta(days=i * 30)
            month_start = date(month_date.year, month_date.month, 1)
            if month_date.month == 12:
                month_end = date(month_date.year + 1, 1, 1)
            else:
                month_end = date(month_date.year, month_date.month + 1, 1)

            month_count = db.query(Borrow).filter(
                Borrow.created_at >= month_start,
                Borrow.created_at < month_end,
            ).count()

            monthly_trend.append({
                "month": month_start.strftime("%Y-%m"),
                "count": month_count,
            })

        return BorrowStatsReport(
            total=total,
            pending=pending,
            approved=approved,
            rejected=rejected,
            returned=returned,
            overdue=overdue,
            monthly_trend=monthly_trend,
        )

    @staticmethod
    def get_category_stats(db: Session) -> CategoryStatsReport:
        """获取分类统计报告"""
        categories = []
        category_stats = db.query(
            Category.id,
            Category.name,
            Category.icon,
            func.count(Asset.id).label("asset_count"),
        ).outerjoin(Asset, Asset.category_id == Category.id) \
         .group_by(Category.id, Category.name, Category.icon) \
         .all()

        for cat_id, cat_name, cat_icon, asset_count in category_stats:
            # 计算各状态数量
            status_counts = db.query(Asset.status, func.count(Asset.id)) \
                              .filter(Asset.category_id == cat_id) \
                              .group_by(Asset.status).all()
            status_breakdown = {s: c for s, c in status_counts}

            categories.append({
                "id": cat_id,
                "name": cat_name,
                "icon": cat_icon,
                "total": asset_count,
                "by_status": status_breakdown,
            })

        return CategoryStatsReport(categories=categories)
