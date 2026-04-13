"""资产管理API端点"""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from io import BytesIO
from ..database import get_db
from ..schemas.asset import AssetCreate, AssetUpdate, AssetResponse
from ..schemas.common import PagedResponse
from ..services.asset_service import AssetService
from ..api.deps import get_current_user, get_admin_user
from ..models.user import User

router = APIRouter()


@router.get("", summary="获取资产列表")
async def list_assets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取资产列表，支持分页、搜索和筛选"""
    service = AssetService(db)
    return service.list_assets(page, page_size, keyword, status, category_id)


@router.get("/stats", summary="获取资产统计")
async def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取资产统计数据"""
    service = AssetService(db)
    return service.get_stats()


@router.get("/{asset_id}", response_model=AssetResponse, summary="获取资产详情")
async def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单个资产详情"""
    service = AssetService(db)
    return service.get_asset(asset_id)


@router.post("", response_model=AssetResponse, summary="新增资产")
async def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """新增资产（需要管理员权限）"""
    service = AssetService(db)
    return service.create_asset(asset, current_user)


@router.put("/{asset_id}", response_model=AssetResponse, summary="修改资产")
async def update_asset(
    asset_id: int,
    asset: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """修改资产信息（需要管理员权限）"""
    service = AssetService(db)
    return service.update_asset(asset_id, asset, current_user)


@router.delete("/{asset_id}", summary="删除资产")
async def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """删除资产（需要管理员权限）"""
    service = AssetService(db)
    service.delete_asset(asset_id, current_user)
    return {"message": "删除成功"}


@router.post("/import", summary="批量导入资产")
async def import_assets(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """从Excel文件批量导入资产"""
    content = await file.read()
    service = AssetService(db)
    return service.import_assets(content, current_user)
