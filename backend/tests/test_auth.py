# 认证API测试
import pytest


class TestAuth:
    """认证相关测试"""

    def test_login_success(self, client, admin_user):
        """测试管理员登录成功"""
        response = client.post("/api/auth/login", json={
            "username": "test_admin",
            "password": "admin123"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "token" in data["data"]
        assert "access_token" in data["data"]["token"]
        assert "refresh_token" in data["data"]["token"]
        assert data["data"]["user"]["username"] == "test_admin"

    def test_login_wrong_password(self, client, admin_user):
        """测试密码错误登录失败"""
        response = client.post("/api/auth/login", json={
            "username": "test_admin",
            "password": "wrong_password"
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """测试用户不存在登录失败"""
        response = client.post("/api/auth/login", json={
            "username": "nonexistent",
            "password": "password123"
        })
        assert response.status_code == 401

    def test_get_me_with_valid_token(self, client, admin_token):
        """测试有效令牌获取当前用户信息"""
        response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["username"] == "test_admin"
        assert data["data"]["role"] == "admin"

    def test_get_me_without_token(self, client, admin_user):
        """测试无令牌访问受保护接口"""
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_get_me_with_invalid_token(self, client):
        """测试无效令牌访问受保护接口"""
        response = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401

    def test_refresh_token(self, client, admin_user):
        """测试刷新令牌"""
        # 先登录获取刷新令牌
        login_response = client.post("/api/auth/login", json={
            "username": "test_admin",
            "password": "admin123"
        })
        refresh_token = login_response.json()["data"]["token"]["refresh_token"]

        # 使用刷新令牌获取新的访问令牌
        response = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data["data"]

    def test_refresh_with_invalid_token(self, client):
        """测试使用无效刷新令牌"""
        response = client.post("/api/auth/refresh", json={"refresh_token": "invalid_refresh_token"})
        assert response.status_code == 401

    def test_logout(self, client, admin_token, admin_user):
        """测试退出登录"""
        response = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert response.json()["message"] == "退出登录成功"

    def test_login_inactive_user(self, client, db):
        """测试禁用用户无法登录"""
        from app.models.user import User
        from app.utils.security import hash_password
        from app.constants.role import UserRole

        inactive_user = User(
            username="inactive_user",
            email="inactive@test.com",
            password_hash=hash_password("password123"),
            full_name="禁用用户",
            role=UserRole.USER,
            is_active=False,
        )
        db.add(inactive_user)
        db.commit()

        response = client.post("/api/auth/login", json={
            "username": "inactive_user",
            "password": "password123"
        })
        assert response.status_code == 401
