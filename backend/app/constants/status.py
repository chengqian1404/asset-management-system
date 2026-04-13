# 资产状态枚举定义
from enum import Enum


class AssetStatus(str, Enum):
    IN_USE = "in_use"              # 在用
    IDLE = "idle"                  # 闲置
    MAINTENANCE = "maintenance"    # 维修中
    SCRAPPED = "scrapped"          # 已报废
    BORROWED = "borrowed"          # 已借出
