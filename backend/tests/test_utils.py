"""工具模块测试"""
import pytest
from app.utils.security import hash_password, verify_password, create_access_token, decode_token
from app.utils.validators import validate_asset_number, validate_email


def test_password_hashing():
    """测试密码哈希"""
    password = "test123"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_token():
    """测试JWT Token"""
    token = create_access_token({"sub": "testuser"})
    payload = decode_token(token)
    assert payload["sub"] == "testuser"


def test_validate_asset_number():
    """测试资产编号验证"""
    assert validate_asset_number("IT-0001")
    assert not validate_asset_number("invalid")


def test_validate_email():
    """测试邮箱验证"""
    assert validate_email("test@example.com")
    assert not validate_email("invalid-email")
