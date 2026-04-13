# 资产管理API测试
import pytest
from app.constants.status import AssetStatus


class TestAsset:
    """资产管理相关测试"""

    def test_get_assets_authenticated(self, client, admin_token, test_asset):
        """测试已认证用户可获取资产列表"""
        response = client.get("/api/assets", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["total"] >= 1
        assert len(data["data"]["items"]) >= 1

    def test_get_assets_unauthenticated(self, client):
        """测试未认证用户无法获取资产列表"""
        response = client.get("/api/assets")
        assert response.status_code == 401

    def test_get_asset_stats(self, client, admin_token, test_asset):
        """测试获取资产统计数据"""
        response = client.get("/api/assets/stats", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert "total" in data
        assert "idle" in data
        assert data["total"] >= 1

    def test_create_asset_as_admin(self, client, admin_token, test_category):
        """测试管理员创建资产"""
        response = client.post("/api/assets", json={
            "asset_number": "NEW-001",
            "name": "新测试资产",
            "category_id": test_category.id,
            "status": "idle",
            "location": "测试室A",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["asset_number"] == "NEW-001"
        assert data["name"] == "新测试资产"

    def test_create_asset_as_approver(self, client, approver_token, test_category):
        """测试审批人也可以创建资产"""
        response = client.post("/api/assets", json={
            "asset_number": "APP-001",
            "name": "审批人创建的资产",
            "category_id": test_category.id,
            "status": "idle",
        }, headers={"Authorization": f"Bearer {approver_token}"})
        assert response.status_code == 200

    def test_create_asset_as_user_forbidden(self, client, user_token, test_category):
        """测试普通用户无法创建资产"""
        response = client.post("/api/assets", json={
            "asset_number": "USER-001",
            "name": "用户创建的资产",
            "status": "idle",
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403

    def test_create_asset_duplicate_number(self, client, admin_token, test_asset, test_category):
        """测试重复资产编号创建失败"""
        response = client.post("/api/assets", json={
            "asset_number": "TEST-001",  # 已存在的编号
            "name": "重复编号资产",
            "status": "idle",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 409

    def test_get_asset_detail(self, client, admin_token, test_asset):
        """测试获取资产详情"""
        response = client.get(f"/api/assets/{test_asset.id}", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["id"] == test_asset.id
        assert data["asset_number"] == "TEST-001"

    def test_get_asset_not_found(self, client, admin_token):
        """测试获取不存在的资产"""
        response = client.get("/api/assets/99999", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 404

    def test_update_asset(self, client, admin_token, test_asset):
        """测试更新资产信息"""
        response = client.put(f"/api/assets/{test_asset.id}", json={
            "name": "更新后的资产名称",
            "location": "新位置",
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["name"] == "更新后的资产名称"
        assert data["location"] == "新位置"

    def test_delete_asset_as_admin(self, client, admin_token, test_category, db):
        """测试管理员删除资产"""
        from app.models.asset import Asset
        asset = Asset(
            asset_number="DEL-001",
            name="待删除资产",
            category_id=test_category.id,
            status=AssetStatus.IDLE,
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)

        response = client.delete(f"/api/assets/{asset.id}", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200

    def test_delete_asset_as_user_forbidden(self, client, user_token, test_asset):
        """测试普通用户无法删除资产"""
        response = client.delete(f"/api/assets/{test_asset.id}", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403

    def test_get_assets_with_search(self, client, admin_token, test_asset):
        """测试资产列表搜索功能"""
        response = client.get("/api/assets?search=测试资产", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["total"] >= 1

    def test_get_assets_with_status_filter(self, client, admin_token, test_asset):
        """测试按状态筛选资产"""
        response = client.get("/api/assets?status=idle", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        # 所有返回的资产状态应该是idle
        for item in data["items"]:
            assert item["status"] == "idle"

    def test_get_assets_pagination(self, client, admin_token, test_asset):
        """测试资产分页功能"""
        response = client.get("/api/assets?page=1&page_size=5", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["page"] == 1
        assert data["page_size"] == 5
