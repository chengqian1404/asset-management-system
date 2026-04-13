# 用户角色枚举定义
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"        # 管理员 - 拥有所有权限
    APPROVER = "approver"  # 审批人 - 可审批借用申请
    USER = "user"          # 普通用户 - 可查看资产和申请借用
