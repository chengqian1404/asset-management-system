# 数据验证工具模块
import re
from typing import Optional


def validate_asset_number(asset_number: str) -> bool:
    """验证资产编号格式（字母数字和连字符，3-50字符）"""
    pattern = r'^[A-Za-z0-9\-\_]{3,50}$'
    return bool(re.match(pattern, asset_number))


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username: str) -> bool:
    """验证用户名格式（字母数字和下划线，3-50字符）"""
    pattern = r'^[A-Za-z0-9_]{3,50}$'
    return bool(re.match(pattern, username))


def validate_phone(phone: str) -> bool:
    """验证中国手机号格式"""
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))


def sanitize_string(value: Optional[str]) -> Optional[str]:
    """清理字符串，去除首尾空格，空字符串转为None"""
    if value is None:
        return None
    stripped = value.strip()
    return stripped if stripped else None
