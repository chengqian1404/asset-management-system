"""报表业务逻辑"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.asset import Asset
from ..models.borrow import Borrow
from ..models.category import Category
from ..constants.status import AssetStatus, BorrowStatus


class ReportService:
    """报表业务逻辑"""

    def __init__(self, db: Session):
        self.db = db

    def asset_stats(self):
        """资产统计报表"""
        total = self.db.query(Asset).count()

        status_counts = {}
        for status_val in [AssetStatus.IN_USE, AssetStatus.IDLE,
                           AssetStatus.MAINTENANCE, AssetStatus.SCRAPPED, AssetStatus.BORROWED]:
            count = self.db.query(Asset).filter(Asset.status == status_val).count()
            status_counts[status_val] = count

        return {
            "total": total,
            "by_status": status_counts,
        }

    def borrow_stats(self):
        """借用统计报表"""
        total = self.db.query(Borrow).count()

        status_counts = {}
        for status_val in [BorrowStatus.PENDING, BorrowStatus.APPROVED,
                           BorrowStatus.REJECTED, BorrowStatus.RETURNED]:
            count = self.db.query(Borrow).filter(Borrow.status == status_val).count()
            status_counts[status_val] = count

        return {
            "total": total,
            "by_status": status_counts,
            "pending": status_counts.get(BorrowStatus.PENDING, 0),
        }

    def category_stats(self):
        """分类统计"""
        results = self.db.query(
            Category.name,
            func.count(Asset.id).label("asset_count")
        ).outerjoin(Asset, Asset.category_id == Category.id).group_by(Category.id).all()

        return [
            {"category": row[0], "count": row[1]}
            for row in results
        ]
