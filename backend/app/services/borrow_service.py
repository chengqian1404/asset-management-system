"""借用业务逻辑"""
from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.borrow import Borrow
from ..models.asset import Asset
from ..models.user import User
from ..schemas.borrow import BorrowCreate, BorrowApprove
from ..constants.messages import Messages
from ..constants.status import BorrowStatus, AssetStatus


class BorrowService:
    """借用管理业务逻辑"""

    def __init__(self, db: Session):
        self.db = db

    def list_borrows(self, page: int, page_size: int, status=None, current_user=None):
        """获取借用列表"""
        query = self.db.query(Borrow)

        # 非管理员只能看到自己的记录
        if current_user and current_user.role == "user":
            query = query.filter(Borrow.user_id == current_user.id)

        if status:
            query = query.filter(Borrow.status == status)

        total = query.count()
        borrows = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            "data": borrows,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def my_borrows(self, page: int, page_size: int, current_user: User):
        """获取我的借用记录"""
        query = self.db.query(Borrow).filter(Borrow.user_id == current_user.id)
        total = query.count()
        borrows = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            "data": borrows,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def create_borrow(self, borrow_data: BorrowCreate, current_user: User) -> Borrow:
        """创建借用申请"""
        asset = self.db.query(Asset).filter(Asset.id == borrow_data.asset_id).first()
        if not asset:
            raise HTTPException(status_code=404, detail=Messages.ASSET_NOT_FOUND)

        if asset.status not in [AssetStatus.IDLE, AssetStatus.IN_USE]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Messages.BORROW_ASSET_UNAVAILABLE
            )

        borrow = Borrow(
            asset_id=borrow_data.asset_id,
            user_id=current_user.id,
            reason=borrow_data.reason,
            expected_return_date=borrow_data.expected_return_date,
            status=BorrowStatus.PENDING,
        )
        self.db.add(borrow)
        self.db.commit()
        self.db.refresh(borrow)
        return borrow

    def approve_borrow(self, borrow_id: int, approve_data: BorrowApprove, current_user: User) -> Borrow:
        """审批借用申请"""
        borrow = self.db.query(Borrow).filter(Borrow.id == borrow_id).first()
        if not borrow:
            raise HTTPException(status_code=404, detail=Messages.BORROW_NOT_FOUND)

        if borrow.status != BorrowStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="只能审批待审批状态的申请"
            )

        borrow.approver_id = current_user.id

        if approve_data.approve:
            borrow.status = BorrowStatus.APPROVED
            # 更新资产状态为借出
            asset = self.db.query(Asset).filter(Asset.id == borrow.asset_id).first()
            if asset:
                asset.status = AssetStatus.BORROWED
        else:
            borrow.status = BorrowStatus.REJECTED

        self.db.commit()
        self.db.refresh(borrow)
        return borrow

    def return_asset(self, borrow_id: int, current_user: User) -> Borrow:
        """归还资产"""
        borrow = self.db.query(Borrow).filter(Borrow.id == borrow_id).first()
        if not borrow:
            raise HTTPException(status_code=404, detail=Messages.BORROW_NOT_FOUND)

        if borrow.status == BorrowStatus.RETURNED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Messages.BORROW_ALREADY_RETURNED
            )

        borrow.status = BorrowStatus.RETURNED
        borrow.actual_return_date = date.today()

        # 更新资产状态为闲置
        asset = self.db.query(Asset).filter(Asset.id == borrow.asset_id).first()
        if asset:
            asset.status = AssetStatus.IDLE

        self.db.commit()
        self.db.refresh(borrow)
        return borrow
