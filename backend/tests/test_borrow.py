"""借用模块测试"""
import pytest


def test_create_borrow(client, admin_token):
    """测试创建借用申请"""
    # 先创建资产
    asset_response = client.post(
        "/api/assets",
        json={"asset_number": "BW-0001", "name": "借用测试资产", "status": "idle"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    asset_id = asset_response.json()["id"]

    response = client.post(
        "/api/borrows",
        json={"asset_id": asset_id, "reason": "工作需要"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "pending"
