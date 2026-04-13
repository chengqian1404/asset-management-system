# 综合API测试
import pytest


class TestSystem:
    """系统管理API测试"""

    def test_health_check(self, client):
        """测试系统健康检查接口（无需认证）"""
        response = client.get("/api/system/health")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["status"] == "healthy"

    def test_root_endpoint(self, client):
        """测试根路径接口"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "app" in data
        assert "version" in data

    def test_get_settings_as_admin(self, client, admin_token):
        """测试管理员获取系统设置"""
        response = client.get("/api/system/settings",
                               headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200

    def test_get_settings_as_user_forbidden(self, client, user_token):
        """测试普通用户无法获取系统设置"""
        response = client.get("/api/system/settings",
                               headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403

    def test_get_logs_as_admin(self, client, admin_token):
        """测试管理员获取操作日志"""
        response = client.get("/api/system/logs",
                               headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert "total" in data
        assert "items" in data


class TestCategory:
    """分类管理API测试"""

    def test_get_categories(self, client, user_token, test_category):
        """测试获取分类列表"""
        response = client.get("/api/categories",
                               headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) >= 1
        assert data[0]["asset_count"] is not None

    def test_create_category_as_admin(self, client, admin_token):
        """测试管理员创建分类"""
        response = client.post("/api/categories", json={
            "name": "新测试分类",
            "description": "测试描述",
            "icon": "test-icon",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["name"] == "新测试分类"

    def test_create_category_as_user_forbidden(self, client, user_token):
        """测试普通用户无法创建分类"""
        response = client.post("/api/categories", json={
            "name": "用户创建分类",
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403

    def test_create_duplicate_category(self, client, admin_token, test_category):
        """测试创建重名分类失败"""
        response = client.post("/api/categories", json={
            "name": "测试设备",  # 已存在
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 409

    def test_update_category(self, client, admin_token, test_category):
        """测试更新分类信息"""
        response = client.put(f"/api/categories/{test_category.id}", json={
            "description": "更新后的描述",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["description"] == "更新后的描述"

    def test_delete_empty_category(self, client, admin_token, db):
        """测试删除无资产的分类"""
        from app.models.category import Category
        empty_cat = Category(name="空分类删除测试", description="测试")
        db.add(empty_cat)
        db.commit()
        db.refresh(empty_cat)

        response = client.delete(f"/api/categories/{empty_cat.id}",
                                  headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200

    def test_delete_category_with_assets_fails(self, client, admin_token, test_category, test_asset):
        """测试有资产的分类无法删除"""
        response = client.delete(f"/api/categories/{test_category.id}",
                                  headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 400
