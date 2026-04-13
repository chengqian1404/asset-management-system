"""系统管理API端点"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..api.deps import get_current_user, get_admin_user
from ..models.user import User
from ..models.operation_log import OperationLog

router = APIRouter()


@router.get("/settings", summary="获取系统设置")
async def get_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """获取系统设置"""
    return {"settings": {"app_name": "资产管理系统", "version": "1.0.0"}}


@router.get("/logs", summary="获取操作日志")
async def get_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """获取系统操作日志"""
    total = db.query(OperationLog).count()
    logs = db.query(OperationLog).order_by(
        OperationLog.created_at.desc()
    ).offset((page - 1) * page_size).limit(page_size).all()

    return {
        "data": [
            {
                "id": log.id,
                "action": log.action,
                "table_name": log.table_name,
                "record_id": log.record_id,
                "created_at": log.created_at,
            }
            for log in logs
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }
