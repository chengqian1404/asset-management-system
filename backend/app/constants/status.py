"""资产状态常量"""


class AssetStatus:
    IN_USE = "in_use"            # 在用
    IDLE = "idle"                # 闲置
    MAINTENANCE = "maintenance"  # 维修中
    SCRAPPED = "scrapped"        # 已报废
    BORROWED = "borrowed"        # 借出中


class BorrowStatus:
    PENDING = "pending"      # 待审批
    APPROVED = "approved"    # 已审批
    REJECTED = "rejected"    # 已拒绝
    RETURNED = "returned"    # 已归还
    OVERDUE = "overdue"      # 已逾期


ASSET_STATUS_LABELS = {
    AssetStatus.IN_USE: "在用",
    AssetStatus.IDLE: "闲置",
    AssetStatus.MAINTENANCE: "维修中",
    AssetStatus.SCRAPPED: "已报废",
    AssetStatus.BORROWED: "借出中",
}

BORROW_STATUS_LABELS = {
    BorrowStatus.PENDING: "待审批",
    BorrowStatus.APPROVED: "已审批",
    BorrowStatus.REJECTED: "已拒绝",
    BorrowStatus.RETURNED: "已归还",
    BorrowStatus.OVERDUE: "已逾期",
}
