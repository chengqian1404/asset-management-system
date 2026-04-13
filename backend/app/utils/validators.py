"""验证工具"""
import re


def validate_asset_number(asset_number: str) -> bool:
    """验证资产编号格式"""
    pattern = r'^[A-Z]{2,4}-\d{4,8}$'
    return bool(re.match(pattern, asset_number))


def validate_phone(phone: str) -> bool:
    """验证手机号码"""
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
