# 用户管理API测试
import pytest


class TestUser:
    """用户管理相关测试"""

    def test_get_users_as_admin(self, client, admin_token, admin_user):
        """测试管理员获取用户列表"""
        response = client.get("/api/users", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["total"] >= 1

    def test_get_users_as_normal_user_forbidden(self, client, user_token):
        """测试普通用户无法获取用户列表"""
        response = client.get("/api/users", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403

    def test_create_user_as_admin(self, client, admin_token):
        """测试管理员创建用户"""
        response = client.post("/api/users", json={
            "username": "new_test_user",
            "email": "new_test@test.com",
            "password": "password123",
            "full_name": "新测试用户",
            "role": "user",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["username"] == "new_test_user"
        assert data["role"] == "user"

    def test_create_user_duplicate_username(self, client, admin_token, admin_user):
        """测试创建重复用户名失败"""
        response = client.post("/api/users", json={
            "username": "test_admin",  # 已存在
            "email": "unique@test.com",
            "password": "password123",
            "full_name": "重复用户名",
            "role": "user",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 409

    def test_create_user_duplicate_email(self, client, admin_token, admin_user):
        """测试创建重复邮箱失败"""
        response = client.post("/api/users", json={
            "username": "unique_username",
            "email": "admin@test.com",  # 已存在
            "password": "password123",
            "full_name": "重复邮箱",
            "role": "user",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 409

    def test_update_user(self, client, admin_token, normal_user):
        """测试管理员更新用户信息"""
        response = client.put(f"/api/users/{normal_user.id}", json={
            "full_name": "更新后的姓名",
            "department": "新部门",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["full_name"] == "更新后的姓名"
        assert data["department"] == "新部门"

    def test_delete_user_as_admin(self, client, admin_token, normal_user):
        """测试管理员删除用户"""
        response = client.delete(f"/api/users/{normal_user.id}",
                                  headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200

    def test_cannot_delete_self(self, client, admin_token, admin_user):
        """测试管理员不能删除自己"""
        response = client.delete(f"/api/users/{admin_user.id}",
                                  headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 400

    def test_get_user_permissions_admin(self, client, admin_token, admin_user):
        """测试获取管理员权限"""
        response = client.get(f"/api/users/{admin_user.id}/permissions",
                               headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["can_manage_users"] is True
        assert data["can_approve_borrows"] is True
        assert data["can_manage_system"] is True

    def test_get_user_permissions_normal_user(self, client, user_token, normal_user):
        """测试获取普通用户权限"""
        response = client.get(f"/api/users/{normal_user.id}/permissions",
                               headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["can_manage_users"] is False
        assert data["can_approve_borrows"] is False

    def test_user_cannot_view_others_permissions(self, client, user_token, admin_user):
        """测试普通用户不能查看其他用户的权限"""
        response = client.get(f"/api/users/{admin_user.id}/permissions",
                               headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403
