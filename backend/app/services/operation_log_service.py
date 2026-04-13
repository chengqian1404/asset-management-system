# 操作日志服务
import json
from typing import Optional, Any, Dict
from sqlalchemy.orm import Session
from app.models.operation_log import OperationLog


class OperationLogService:
    """操作日志服务类"""

    @staticmethod
    def log(
        db: Session,
        action: str,
        user_id: Optional[int] = None,
        table_name: Optional[str] = None,
        record_id: Optional[int] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
    ) -> OperationLog:
        """记录操作日志"""
        log_entry = OperationLog(
            user_id=user_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
            old_values=json.dumps(old_values, ensure_ascii=False, default=str) if old_values else None,
            new_values=json.dumps(new_values, ensure_ascii=False, default=str) if new_values else None,
            ip_address=ip_address,
        )
        db.add(log_entry)
        db.flush()  # 立即写入但不提交，由外层事务统一提交
        return log_entry

    @staticmethod
    def get_logs(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
    ) -> tuple:
        """分页获取操作日志"""
        query = db.query(OperationLog)

        if user_id:
            query = query.filter(OperationLog.user_id == user_id)
        if action:
            query = query.filter(OperationLog.action == action)

        total = query.count()
        logs = query.order_by(OperationLog.created_at.desc()) \
                    .offset((page - 1) * page_size) \
                    .limit(page_size) \
                    .all()

        return total, logs
