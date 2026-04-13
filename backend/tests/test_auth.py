"""认证模块测试"""
import pytest
from fastapi.testclient import TestClient


def test_login_success(client, admin_token):
    """测试登录成功"""
    response = client.post("/api/auth/login", json={
        "username": "testadmin",
        "password": "admin123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_failure(client, admin_token):
    """测试登录失败"""
    response = client.post("/api/auth/login", json={
        "username": "testadmin",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_get_me(client, admin_token):
    """测试获取当前用户"""
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testadmin"
