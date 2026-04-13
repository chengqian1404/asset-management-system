# 系统管理API路由
import os
import shutil
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.common import SuccessResponse, PaginationResponse
from app.services.operation_log_service import OperationLogService
from app.api.deps import get_current_active_user, require_admin
from app.models.user import User
from app.models.system_setting import SystemSetting
from app.config import settings

router = APIRouter(prefix="/system", tags=["系统管理"])


@router.get("/health", response_model=SuccessResponse, summary="健康检查")
def health_check(db: Session = Depends(get_db)):
    """系统健康检查，验证数据库连接"""
    try:
        db.execute(text("SELECT 1"))
        return SuccessResponse(
            message="系统运行正常",
            data={
                "status": "healthy",
                "database": "connected",
                "version": settings.APP_VERSION,
                "timestamp": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        return SuccessResponse(
            code=500,
            message="数据库连接异常",
            data={"status": "unhealthy", "error": str(e)}
        )


@router.get("/settings", response_model=SuccessResponse, summary="获取系统设置")
def get_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """获取所有系统设置（仅管理员）"""
    settings_list = db.query(SystemSetting).all()
    settings_dict = {s.key: s.value for s in settings_list}
    return SuccessResponse(data=settings_dict)


@router.put("/settings", response_model=SuccessResponse, summary="更新系统设置")
def update_settings(
    settings_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """批量更新系统设置（仅管理员）"""
    for key, value in settings_data.items():
        existing = db.query(SystemSetting).filter(SystemSetting.key == key).first()
        if existing:
            existing.value = str(value)
        else:
            db.add(SystemSetting(key=key, value=str(value)))

    db.commit()
    return SuccessResponse(message="系统设置更新成功")


@router.post("/backup", response_model=SuccessResponse, summary="备份数据库")
def backup_database(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """备份SQLite数据库文件（仅管理员）"""
    try:
        # 确保备份目录存在
        os.makedirs(settings.BACKUP_DIR, exist_ok=True)

        # 生成备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.db"
        backup_path = os.path.join(settings.BACKUP_DIR, backup_filename)

        # 获取源数据库路径
        db_url = settings.DATABASE_URL
        if db_url.startswith("sqlite:///"):
            source_path = db_url.replace("sqlite:///", "")
            if os.path.exists(source_path):
                shutil.copy2(source_path, backup_path)
                return SuccessResponse(
                    message="数据库备份成功",
                    data={"backup_file": backup_filename, "path": backup_path}
                )

        return SuccessResponse(code=400, message="备份失败：无法找到数据库文件")
    except Exception as e:
        return SuccessResponse(code=500, message=f"备份失败：{str(e)}")


@router.post("/restore", response_model=SuccessResponse, summary="恢复数据库")
def restore_database(
    backup_file: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """从备份文件恢复数据库（仅管理员）"""
    try:
        # 安全过滤：只允许不含路径分隔符的纯文件名，防止路径注入
        safe_filename = os.path.basename(backup_file)
        if not safe_filename or safe_filename != backup_file:
            return SuccessResponse(code=400, message="无效的备份文件名")

        # 构造绝对路径并验证文件在允许目录内（使用 commonpath 跨平台兼容）
        backup_dir_abs = os.path.realpath(settings.BACKUP_DIR)
        backup_path_abs = os.path.realpath(os.path.join(backup_dir_abs, safe_filename))
        try:
            common = os.path.commonpath([backup_dir_abs, backup_path_abs])
        except ValueError:
            common = ""
        if common != backup_dir_abs:
            return SuccessResponse(code=400, message="非法的备份文件路径")

        if not os.path.exists(backup_path_abs):
            return SuccessResponse(code=404, message="备份文件不存在")

        db_url = settings.DATABASE_URL
        if db_url.startswith("sqlite:///"):
            target_path = db_url.replace("sqlite:///", "")
            shutil.copy2(backup_path_abs, target_path)
            return SuccessResponse(message="数据库恢复成功")

        return SuccessResponse(code=400, message="恢复失败：数据库类型不支持")
    except Exception as e:
        return SuccessResponse(code=500, message=f"恢复失败：{str(e)}")


@router.get("/logs", response_model=SuccessResponse, summary="获取操作日志")
def get_logs(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    user_id: Optional[int] = Query(None, description="按用户筛选"),
    action: Optional[str] = Query(None, description="按操作类型筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """获取系统操作日志（仅管理员）"""
    total, logs = OperationLogService.get_logs(db, page, page_size, user_id, action)
    items = []
    for log in logs:
        items.append({
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "table_name": log.table_name,
            "record_id": log.record_id,
            "ip_address": log.ip_address,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        })
    return SuccessResponse(
        data=PaginationResponse(total=total, page=page, page_size=page_size, items=items)
    )
