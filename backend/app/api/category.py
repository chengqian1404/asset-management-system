# 分类管理API路由
from typing import Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.category import Category
from app.models.asset import Asset
from app.schemas.common import SuccessResponse
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.operation_log_service import OperationLogService
from app.api.deps import get_current_active_user, require_admin
from app.models.user import User
from app.utils.exceptions import NotFoundError, ConflictError, BusinessError

router = APIRouter(prefix="/categories", tags=["资产分类"])


@router.get("", response_model=SuccessResponse, summary="获取分类列表")
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取所有资产分类及各分类下资产数量"""
    categories = db.query(Category).all()
    result = []
    for cat in categories:
        asset_count = db.query(func.count(Asset.id)).filter(Asset.category_id == cat.id).scalar()
        cat_data = CategoryResponse.model_validate(cat).model_dump()
        cat_data["asset_count"] = asset_count
        result.append(cat_data)
    return SuccessResponse(data=result)


@router.post("", response_model=SuccessResponse, summary="创建分类")
def create_category(
    category_data: CategoryCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """创建新资产分类（仅管理员）"""
    if db.query(Category).filter(Category.name == category_data.name).first():
        raise ConflictError("分类名称已存在")

    category = Category(**category_data.model_dump())
    db.add(category)
    db.flush()

    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="create_category", user_id=current_user.id,
        table_name="categories", record_id=category.id,
        new_values={"name": category.name}, ip_address=ip,
    )
    db.commit()
    db.refresh(category)

    cat_data = CategoryResponse.model_validate(category).model_dump()
    cat_data["asset_count"] = 0
    return SuccessResponse(message="分类创建成功", data=cat_data)


@router.put("/{category_id}", response_model=SuccessResponse, summary="更新分类")
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """更新分类信息（仅管理员）"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise NotFoundError("分类不存在")

    # 检查名称唯一性
    if category_data.name and category_data.name != category.name:
        if db.query(Category).filter(Category.name == category_data.name, Category.id != category_id).first():
            raise ConflictError("分类名称已存在")

    old_values = CategoryResponse.model_validate(category).model_dump()
    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="update_category", user_id=current_user.id,
        table_name="categories", record_id=category_id,
        old_values=old_values, ip_address=ip,
    )
    db.commit()
    db.refresh(category)

    asset_count = db.query(func.count(Asset.id)).filter(Asset.category_id == category_id).scalar()
    cat_data = CategoryResponse.model_validate(category).model_dump()
    cat_data["asset_count"] = asset_count
    return SuccessResponse(message="分类更新成功", data=cat_data)


@router.delete("/{category_id}", response_model=SuccessResponse, summary="删除分类")
def delete_category(
    category_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """删除分类（仅管理员，该分类下无资产时才能删除）"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise NotFoundError("分类不存在")

    # 检查该分类下是否有资产
    asset_count = db.query(func.count(Asset.id)).filter(Asset.category_id == category_id).scalar()
    if asset_count > 0:
        raise BusinessError(f"该分类下有 {asset_count} 个资产，无法删除")

    old_values = {"name": category.name}
    db.delete(category)

    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="delete_category", user_id=current_user.id,
        table_name="categories", record_id=category_id,
        old_values=old_values, ip_address=ip,
    )
    db.commit()
    return SuccessResponse(message="分类删除成功")
