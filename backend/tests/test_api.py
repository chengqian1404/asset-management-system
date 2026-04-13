"""API集成测试"""
import pytest


def test_health_check(client):
    """测试健康检查接口"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_unauthorized_access(client):
    """测试未授权访问"""
    response = client.get("/api/assets")
    assert response.status_code == 403


def test_categories_crud(client, admin_token):
    """测试分类CRUD"""
    # 创建
    response = client.post(
        "/api/categories",
        json={"name": "电子设备", "description": "电脑、平板等"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    category_id = response.json()["id"]

    # 获取列表
    response = client.get(
        "/api/categories",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    # 删除
    response = client.delete(
        f"/api/categories/{category_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
