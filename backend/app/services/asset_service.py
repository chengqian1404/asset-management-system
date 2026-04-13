# 资产服务模块
from typing import Optional, Tuple, List
from sqlalchemy.orm import Session, joinedload
from app.models.asset import Asset
from app.models.category import Category
from app.schemas.asset import AssetCreate, AssetUpdate, AssetStats
from app.utils.exceptions import NotFoundError, ConflictError
from app.utils.qrcode import generate_qr_code
from app.constants.status import AssetStatus


class AssetService:
    """资产管理服务类"""

    @staticmethod
    def get_assets(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        category_id: Optional[int] = None,
        owner_id: Optional[int] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> Tuple[int, List[Asset]]:
        """分页获取资产列表，支持搜索、筛选和排序"""
        query = db.query(Asset).options(
            joinedload(Asset.category),
            joinedload(Asset.owner),
        )

        if search:
            query = query.filter(
                (Asset.name.ilike(f"%{search}%")) |
                (Asset.asset_number.ilike(f"%{search}%")) |
                (Asset.location.ilike(f"%{search}%"))
            )
        if status:
            query = query.filter(Asset.status == status)
        if category_id:
            query = query.filter(Asset.category_id == category_id)
        if owner_id:
            query = query.filter(Asset.owner_id == owner_id)

        # 排序处理
        sort_field = getattr(Asset, sort_by, Asset.created_at)
        if sort_order.lower() == "asc":
            query = query.order_by(sort_field.asc())
        else:
            query = query.order_by(sort_field.desc())

        total = query.count()
        assets = query.offset((page - 1) * page_size).limit(page_size).all()
        return total, assets

    @staticmethod
    def get_asset(db: Session, asset_id: int) -> Asset:
        """根据ID获取资产详情"""
        asset = db.query(Asset).options(
            joinedload(Asset.category),
            joinedload(Asset.owner),
        ).filter(Asset.id == asset_id).first()
        if not asset:
            raise NotFoundError("资产不存在")
        return asset

    @staticmethod
    def create_asset(db: Session, asset_data: AssetCreate) -> Asset:
        """创建新资产"""
        # 检查资产编号唯一性
        if db.query(Asset).filter(Asset.asset_number == asset_data.asset_number).first():
            raise ConflictError("资产编号已存在")

        asset = Asset(**asset_data.model_dump())

        # 生成二维码
        qr_content = f"ASSET:{asset_data.asset_number}"
        asset.qr_code = generate_qr_code(qr_content)

        db.add(asset)
        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def update_asset(db: Session, asset_id: int, asset_data: AssetUpdate) -> Asset:
        """更新资产信息"""
        asset = AssetService.get_asset(db, asset_id)

        update_data = asset_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(asset, field, value)

        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def delete_asset(db: Session, asset_id: int) -> None:
        """删除资产"""
        asset = AssetService.get_asset(db, asset_id)
        db.delete(asset)
        db.commit()

    @staticmethod
    def get_stats(db: Session) -> AssetStats:
        """获取资产统计数据"""
        total = db.query(Asset).count()
        in_use = db.query(Asset).filter(Asset.status == AssetStatus.IN_USE).count()
        idle = db.query(Asset).filter(Asset.status == AssetStatus.IDLE).count()
        maintenance = db.query(Asset).filter(Asset.status == AssetStatus.MAINTENANCE).count()
        scrapped = db.query(Asset).filter(Asset.status == AssetStatus.SCRAPPED).count()
        borrowed = db.query(Asset).filter(Asset.status == AssetStatus.BORROWED).count()

        return AssetStats(
            total=total,
            in_use=in_use,
            idle=idle,
            maintenance=maintenance,
            scrapped=scrapped,
            borrowed=borrowed,
        )

    @staticmethod
    def import_assets(db: Session, assets_data: List[dict]) -> Tuple[int, int, List[str]]:
        """批量导入资产，返回(成功数, 失败数, 错误信息列表)"""
        success_count = 0
        fail_count = 0
        errors = []

        for i, row in enumerate(assets_data, 1):
            try:
                asset_number = row.get("asset_number", "").strip()
                name = row.get("name", "").strip()

                if not asset_number or not name:
                    errors.append(f"第{i}行: 资产编号和名称不能为空")
                    fail_count += 1
                    continue

                # 检查资产编号是否已存在
                if db.query(Asset).filter(Asset.asset_number == asset_number).first():
                    errors.append(f"第{i}行: 资产编号 {asset_number} 已存在")
                    fail_count += 1
                    continue

                # 查找分类
                category_id = None
                if row.get("category_name"):
                    category = db.query(Category).filter(Category.name == row["category_name"]).first()
                    if category:
                        category_id = category.id

                # 处理购买价格
                purchase_price = None
                if row.get("purchase_price"):
                    try:
                        purchase_price = float(row["purchase_price"])
                    except (ValueError, TypeError):
                        pass

                # 处理购买日期
                purchase_date = None
                if row.get("purchase_date"):
                    try:
                        from datetime import date
                        date_str = str(row["purchase_date"])
                        if date_str and date_str != "None":
                            purchase_date = date.fromisoformat(date_str[:10])
                    except (ValueError, TypeError):
                        pass

                asset = Asset(
                    asset_number=asset_number,
                    name=name,
                    category_id=category_id,
                    location=row.get("location"),
                    purchase_date=purchase_date,
                    purchase_price=purchase_price,
                    supplier=row.get("supplier"),
                    description=row.get("description"),
                    status=AssetStatus.IDLE,
                )
                asset.qr_code = generate_qr_code(f"ASSET:{asset_number}")
                db.add(asset)
                success_count += 1

            except Exception as e:
                errors.append(f"第{i}行: 处理失败 - {str(e)}")
                fail_count += 1

        if success_count > 0:
            db.commit()

        return success_count, fail_count, errors
