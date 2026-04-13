# 工具函数单元测试
import pytest
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.utils.validators import validate_asset_number, validate_email, validate_username, sanitize_string
from app.utils.exceptions import NotFoundError, PermissionError, BusinessError, ConflictError


class TestSecurity:
    """安全工具函数测试"""

    def test_hash_password(self):
        """测试密码哈希生成"""
        hashed = hash_password("test_password")
        assert hashed != "test_password"
        assert len(hashed) > 20

    def test_verify_password_correct(self):
        """测试正确密码验证"""
        hashed = hash_password("correct_password")
        assert verify_password("correct_password", hashed) is True

    def test_verify_password_wrong(self):
        """测试错误密码验证失败"""
        hashed = hash_password("correct_password")
        assert verify_password("wrong_password", hashed) is False

    def test_create_access_token(self):
        """测试创建访问令牌"""
        token = create_access_token({"sub": "1", "username": "test"})
        assert token is not None
        assert len(token) > 10

    def test_decode_access_token(self):
        """测试解码访问令牌"""
        token = create_access_token({"sub": "1", "username": "test"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "1"
        assert payload["type"] == "access"

    def test_create_refresh_token(self):
        """测试创建刷新令牌"""
        token = create_refresh_token({"sub": "1", "username": "test"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["type"] == "refresh"

    def test_decode_invalid_token(self):
        """测试解码无效令牌返回None"""
        result = decode_token("invalid.token.here")
        assert result is None


class TestValidators:
    """数据验证函数测试"""

    def test_validate_asset_number_valid(self):
        """测试合法资产编号"""
        assert validate_asset_number("PC-001") is True
        assert validate_asset_number("ASSET_123") is True
        assert validate_asset_number("ABC") is True

    def test_validate_asset_number_invalid(self):
        """测试非法资产编号"""
        assert validate_asset_number("AB") is False         # 太短
        assert validate_asset_number("资产001") is False    # 中文字符
        assert validate_asset_number("A B-001") is False    # 含空格

    def test_validate_email_valid(self):
        """测试合法邮箱格式"""
        assert validate_email("user@example.com") is True
        assert validate_email("test.user+tag@domain.co") is True

    def test_validate_email_invalid(self):
        """测试非法邮箱格式"""
        assert validate_email("not_an_email") is False
        assert validate_email("@domain.com") is False
        assert validate_email("user@") is False

    def test_validate_username_valid(self):
        """测试合法用户名"""
        assert validate_username("user123") is True
        assert validate_username("test_user") is True

    def test_validate_username_invalid(self):
        """测试非法用户名"""
        assert validate_username("ab") is False             # 太短
        assert validate_username("user name") is False      # 含空格
        assert validate_username("用户名") is False         # 中文字符

    def test_sanitize_string_normal(self):
        """测试字符串清理正常情况"""
        assert sanitize_string("  hello  ") == "hello"
        assert sanitize_string("test") == "test"

    def test_sanitize_string_empty(self):
        """测试空字符串转为None"""
        assert sanitize_string("") is None
        assert sanitize_string("   ") is None
        assert sanitize_string(None) is None


class TestExceptions:
    """自定义异常测试"""

    def test_not_found_error(self):
        """测试资源不存在异常"""
        exc = NotFoundError("测试资源不存在")
        assert exc.status_code == 404

    def test_permission_error(self):
        """测试权限不足异常"""
        exc = PermissionError("权限不足")
        assert exc.status_code == 403

    def test_business_error(self):
        """测试业务逻辑异常"""
        exc = BusinessError("业务处理失败")
        assert exc.status_code == 400

    def test_conflict_error(self):
        """测试数据冲突异常"""
        exc = ConflictError("数据冲突")
        assert exc.status_code == 409
