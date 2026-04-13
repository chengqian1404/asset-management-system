"""资产业务逻辑"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.asset import Asset
from ..models.user import User
from ..schemas.asset import AssetCreate, AssetUpdate
from ..utils.qrcode import generate_qrcode
from ..utils.excel import parse_assets_from_excel
from ..constants.messages import Messages
from ..constants.status import AssetStatus


class AssetService:
    """资产管理业务逻辑"""

    def __init__(self, db: Session):
        self.db = db

    def list_assets(self, page: int, page_size: int, keyword=None, status=None, category_id=None):
        """获取资产列表"""
        query = self.db.query(Asset)

        if keyword:
            query = query.filter(
                or_(
                    Asset.name.ilike(f"%{keyword}%"),
                    Asset.asset_number.ilike(f"%{keyword}%"),
                )
            )
        if status:
            query = query.filter(Asset.status == status)
        if category_id:
            query = query.filter(Asset.category_id == category_id)

        total = query.count()
        assets = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            "data": assets,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def get_stats(self):
        """获取资产统计"""
        total = self.db.query(Asset).count()
        in_use = self.db.query(Asset).filter(Asset.status == AssetStatus.IN_USE).count()
        idle = self.db.query(Asset).filter(Asset.status == AssetStatus.IDLE).count()
        maintenance = self.db.query(Asset).filter(Asset.status == AssetStatus.MAINTENANCE).count()
        scrapped = self.db.query(Asset).filter(Asset.status == AssetStatus.SCRAPPED).count()
        borrowed = self.db.query(Asset).filter(Asset.status == AssetStatus.BORROWED).count()

        return {
            "total": total,
            "in_use": in_use,
            "idle": idle,
            "maintenance": maintenance,
            "scrapped": scrapped,
            "borrowed": borrowed,
        }

    def get_asset(self, asset_id: int) -> Asset:
        """获取资产详情"""
        asset = self.db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            raise HTTPException(status_code=404, detail=Messages.ASSET_NOT_FOUND)
        return asset

    def create_asset(self, asset_data: AssetCreate, current_user: User) -> Asset:
        """创建资产"""
        if self.db.query(Asset).filter(Asset.asset_number == asset_data.asset_number).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Messages.ASSET_NUMBER_EXISTS
            )

        qr_data = f"ASSET:{asset_data.asset_number}"
        qr_code = generate_qrcode(qr_data)

        asset = Asset(**asset_data.model_dump(), qr_code=qr_code)
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def update_asset(self, asset_id: int, asset_data: AssetUpdate, current_user: User) -> Asset:
        """更新资产"""
        asset = self.get_asset(asset_id)
        update_data = asset_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(asset, key, value)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def delete_asset(self, asset_id: int, current_user: User):
        """删除资产"""
        asset = self.get_asset(asset_id)
        self.db.delete(asset)
        self.db.commit()

    def import_assets(self, file_content: bytes, current_user: User):
        """批量导入资产"""
        assets_data = parse_assets_from_excel(file_content)
        created = 0
        errors = []

        for i, data in enumerate(assets_data, 1):
            try:
                asset_number = str(data.get("资产编号", ""))
                if not asset_number:
                    errors.append(f"第{i}行：资产编号不能为空")
                    continue

                if self.db.query(Asset).filter(Asset.asset_number == asset_number).first():
                    errors.append(f"第{i}行：资产编号{asset_number}已存在")
                    continue

                asset = Asset(
                    asset_number=asset_number,
                    name=str(data.get("资产名称", "")),
                    status="idle",
                )
                self.db.add(asset)
                created += 1
            except Exception:
                errors.append(f"第{i}行：数据格式错误，请检查后重试")

        self.db.commit()
        return {"created": created, "errors": errors}
