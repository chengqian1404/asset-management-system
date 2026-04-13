# 报告API测试
import pytest


class TestReport:
    """统计报告相关测试"""

    def test_get_asset_stats_report(self, client, admin_token, test_asset):
        """测试获取资产统计报告"""
        response = client.get("/api/reports/asset-stats",
                               headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert "total" in data
        assert "by_status" in data
        assert "by_category" in data
        assert "recent_added" in data
        assert data["total"] >= 1

    def test_get_borrow_stats_report(self, client, admin_token, test_borrow):
        """测试获取借用统计报告"""
        response = client.get("/api/reports/borrow-stats",
                               headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert "total" in data
        assert "pending" in data
        assert "monthly_trend" in data
        assert data["total"] >= 1

    def test_get_category_stats_report(self, client, admin_token, test_category, test_asset):
        """测试获取分类统计报告"""
        response = client.get("/api/reports/category-stats",
                               headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert "categories" in data
        assert len(data["categories"]) >= 1

    def test_report_requires_auth(self, client):
        """测试报告接口需要认证"""
        response = client.get("/api/reports/asset-stats")
        assert response.status_code == 401

    def test_report_accessible_by_user(self, client, user_token, test_asset):
        """测试普通用户也可查看报告"""
        response = client.get("/api/reports/asset-stats",
                               headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200

    def test_borrow_stats_monthly_trend(self, client, admin_token):
        """测试借用统计包含月度趋势数据"""
        response = client.get("/api/reports/borrow-stats",
                               headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        monthly_trend = data["monthly_trend"]
        assert len(monthly_trend) == 6  # 近6个月
        for item in monthly_trend:
            assert "month" in item
            assert "count" in item
