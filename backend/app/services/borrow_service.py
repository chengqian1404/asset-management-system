# 借用服务模块
from datetime import date, datetime, timezone
from typing import Optional, Tuple, List
from sqlalchemy.orm import Session, joinedload
from app.models.borrow import Borrow
from app.models.asset import Asset
from app.schemas.borrow import BorrowCreate
from app.utils.exceptions import NotFoundError, BusinessError, PermissionError
from app.constants.borrow_status import BorrowStatus
from app.constants.status import AssetStatus
from app.constants.role import UserRole


class BorrowService:
    """借用管理服务类"""

    @staticmethod
    def get_borrows(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        user_id: Optional[int] = None,
        asset_id: Optional[int] = None,
    ) -> Tuple[int, List[Borrow]]:
        """分页获取借用记录列表"""
        query = db.query(Borrow).options(
            joinedload(Borrow.asset).joinedload(Asset.category),
            joinedload(Borrow.user),
            joinedload(Borrow.approver),
        )

        if status:
            query = query.filter(Borrow.status == status)
        if user_id:
            query = query.filter(Borrow.user_id == user_id)
        if asset_id:
            query = query.filter(Borrow.asset_id == asset_id)

        total = query.count()
        borrows = query.order_by(Borrow.created_at.desc()) \
                       .offset((page - 1) * page_size) \
                       .limit(page_size) \
                       .all()
        return total, borrows

    @staticmethod
    def get_borrow(db: Session, borrow_id: int) -> Borrow:
        """根据ID获取借用记录详情"""
        borrow = db.query(Borrow).options(
            joinedload(Borrow.asset).joinedload(Asset.category),
            joinedload(Borrow.user),
            joinedload(Borrow.approver),
        ).filter(Borrow.id == borrow_id).first()
        if not borrow:
            raise NotFoundError("借用记录不存在")
        return borrow

    @staticmethod
    def create_borrow(db: Session, borrow_data: BorrowCreate, user_id: int) -> Borrow:
        """创建借用申请"""
        # 检查资产是否存在
        asset = db.query(Asset).filter(Asset.id == borrow_data.asset_id).first()
        if not asset:
            raise NotFoundError("资产不存在")

        # 检查资产状态是否可以借用（只有闲置或在用状态可以申请借用）
        if asset.status not in [AssetStatus.IDLE, AssetStatus.IN_USE]:
            raise BusinessError(f"该资产当前状态为【{asset.status}】，不可申请借用")

        # 检查是否已有待审批的借用申请
        existing = db.query(Borrow).filter(
            Borrow.asset_id == borrow_data.asset_id,
            Borrow.status == BorrowStatus.PENDING,
        ).first()
        if existing:
            raise BusinessError("该资产已有待审批的借用申请")

        borrow = Borrow(
            asset_id=borrow_data.asset_id,
            user_id=user_id,
            reason=borrow_data.reason,
            expected_return_date=borrow_data.expected_return_date,
            status=BorrowStatus.PENDING,
        )
        db.add(borrow)
        db.commit()
        db.refresh(borrow)
        return borrow

    @staticmethod
    def approve_borrow(db: Session, borrow_id: int, approver_id: int) -> Borrow:
        """审批通过借用申请，资产状态变为已借出"""
        borrow = BorrowService.get_borrow(db, borrow_id)

        if borrow.status != BorrowStatus.PENDING:
            raise BusinessError("该借用申请已处理，无法重复审批")

        # 更新借用状态
        borrow.status = BorrowStatus.APPROVED
        borrow.approver_id = approver_id

        # 更新资产状态为已借出
        asset = db.query(Asset).filter(Asset.id == borrow.asset_id).first()
        if asset:
            asset.status = AssetStatus.BORROWED

        db.commit()
        db.refresh(borrow)
        return borrow

    @staticmethod
    def reject_borrow(db: Session, borrow_id: int, approver_id: int) -> Borrow:
        """拒绝借用申请"""
        borrow = BorrowService.get_borrow(db, borrow_id)

        if borrow.status != BorrowStatus.PENDING:
            raise BusinessError("该借用申请已处理，无法重复处理")

        borrow.status = BorrowStatus.REJECTED
        borrow.approver_id = approver_id

        db.commit()
        db.refresh(borrow)
        return borrow

    @staticmethod
    def return_asset(db: Session, borrow_id: int, current_user_id: int, current_user_role: str) -> Borrow:
        """处理资产归还，资产状态变回闲置"""
        borrow = BorrowService.get_borrow(db, borrow_id)

        if borrow.status != BorrowStatus.APPROVED:
            raise BusinessError("借用申请未批准或已归还，无法执行归还操作")

        # 验证归还权限：只有借用人本人、管理员或审批人可以操作
        if (current_user_role not in [UserRole.ADMIN, UserRole.APPROVER] and
                borrow.user_id != current_user_id):
            raise PermissionError("只有借用人本人或管理员可以归还资产")

        # 更新借用状态
        borrow.status = BorrowStatus.RETURNED
        borrow.actual_return_date = date.today()

        # 更新资产状态为闲置
        asset = db.query(Asset).filter(Asset.id == borrow.asset_id).first()
        if asset:
            asset.status = AssetStatus.IDLE

        db.commit()
        db.refresh(borrow)
        return borrow

    @staticmethod
    def check_overdue_borrows(db: Session) -> int:
        """检查并更新逾期借用记录，返回更新数量"""
        today = date.today()
        overdue_borrows = db.query(Borrow).filter(
            Borrow.status == BorrowStatus.APPROVED,
            Borrow.expected_return_date < today,
            Borrow.expected_return_date.isnot(None),
        ).all()

        count = 0
        for borrow in overdue_borrows:
            borrow.status = BorrowStatus.OVERDUE
            count += 1

        if count > 0:
            db.commit()

        return count
