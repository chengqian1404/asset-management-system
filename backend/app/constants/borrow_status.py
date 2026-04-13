# 借用状态枚举定义
from enum import Enum


class BorrowStatus(str, Enum):
    PENDING = "pending"      # 待审批
    APPROVED = "approved"    # 已批准
    REJECTED = "rejected"    # 已拒绝
    RETURNED = "returned"    # 已归还
    OVERDUE = "overdue"      # 已逾期
