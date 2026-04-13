"""资产模块测试"""
import pytest


def test_create_asset(client, admin_token):
    """测试创建资产"""
    response = client.post(
        "/api/assets",
        json={
            "asset_number": "IT-0001",
            "name": "测试电脑",
            "status": "idle",
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "测试电脑"


def test_list_assets(client, admin_token):
    """测试获取资产列表"""
    response = client.get(
        "/api/assets",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert "data" in response.json()


def test_get_asset_stats(client, admin_token):
    """测试获取资产统计"""
    response = client.get(
        "/api/assets/stats",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert "total" in response.json()
