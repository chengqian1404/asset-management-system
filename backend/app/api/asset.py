# 资产管理API路由
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.common import SuccessResponse, PaginationResponse
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse
from app.services.asset_service import AssetService
from app.services.operation_log_service import OperationLogService
from app.api.deps import get_current_active_user, require_admin, require_admin_or_approver
from app.models.user import User
from app.utils.excel import parse_excel_assets

router = APIRouter(prefix="/assets", tags=["资产管理"])


@router.get("/stats", response_model=SuccessResponse, summary="获取资产统计")
def get_asset_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取资产状态统计数据"""
    stats = AssetService.get_stats(db)
    return SuccessResponse(data=stats.model_dump())


@router.get("", response_model=SuccessResponse, summary="获取资产列表")
def get_assets(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    status: Optional[str] = Query(None, description="资产状态筛选"),
    category_id: Optional[int] = Query(None, description="分类ID筛选"),
    owner_id: Optional[int] = Query(None, description="负责人ID筛选"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", description="排序方向"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取资产列表，支持分页、搜索、筛选和排序"""
    total, assets = AssetService.get_assets(
        db, page, page_size, search, status, category_id, owner_id, sort_by, sort_order
    )
    items = [AssetResponse.model_validate(a).model_dump() for a in assets]
    return SuccessResponse(
        data=PaginationResponse(total=total, page=page, page_size=page_size, items=items)
    )


@router.post("", response_model=SuccessResponse, summary="创建资产")
def create_asset(
    asset_data: AssetCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_approver),
):
    """创建新资产（管理员或审批人）"""
    asset = AssetService.create_asset(db, asset_data)
    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="create_asset", user_id=current_user.id,
        table_name="assets", record_id=asset.id,
        new_values={"asset_number": asset.asset_number, "name": asset.name},
        ip_address=ip,
    )
    db.commit()
    return SuccessResponse(message="资产创建成功", data=AssetResponse.model_validate(asset).model_dump())


@router.get("/{asset_id}", response_model=SuccessResponse, summary="获取资产详情")
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取指定资产的详细信息"""
    asset = AssetService.get_asset(db, asset_id)
    return SuccessResponse(data=AssetResponse.model_validate(asset).model_dump())


@router.put("/{asset_id}", response_model=SuccessResponse, summary="更新资产")
def update_asset(
    asset_id: int,
    asset_data: AssetUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_approver),
):
    """更新资产信息（管理员或审批人）"""
    old_asset = AssetService.get_asset(db, asset_id)
    old_values = {"name": old_asset.name, "status": old_asset.status}

    asset = AssetService.update_asset(db, asset_id, asset_data)
    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="update_asset", user_id=current_user.id,
        table_name="assets", record_id=asset_id,
        old_values=old_values,
        new_values={"name": asset.name, "status": asset.status},
        ip_address=ip,
    )
    db.commit()
    return SuccessResponse(message="资产更新成功", data=AssetResponse.model_validate(asset).model_dump())


@router.delete("/{asset_id}", response_model=SuccessResponse, summary="删除资产")
def delete_asset(
    asset_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """删除资产（仅管理员）"""
    old_asset = AssetService.get_asset(db, asset_id)
    old_values = {"asset_number": old_asset.asset_number, "name": old_asset.name}

    AssetService.delete_asset(db, asset_id)
    ip = request.client.host if request.client else None
    OperationLogService.log(
        db=db, action="delete_asset", user_id=current_user.id,
        table_name="assets", record_id=asset_id,
        old_values=old_values, ip_address=ip,
    )
    db.commit()
    return SuccessResponse(message="资产删除成功")


@router.post("/import", response_model=SuccessResponse, summary="批量导入资产")
async def import_assets(
    file: UploadFile = File(..., description="Excel文件"),
    request: Request = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_approver),
):
    """从Excel文件批量导入资产"""
    if not file.filename.endswith((".xlsx", ".xls")):
        from app.utils.exceptions import ValidationError
        raise ValidationError("只支持Excel文件格式(.xlsx, .xls)")

    content = await file.read()
    assets_data = parse_excel_assets(content)
    success_count, fail_count, errors = AssetService.import_assets(db, assets_data)

    return SuccessResponse(
        message=f"导入完成：成功 {success_count} 条，失败 {fail_count} 条",
        data={"success": success_count, "failed": fail_count, "errors": errors}
    )
