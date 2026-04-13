# 借用管理API测试
import pytest
from app.constants.status import AssetStatus
from app.constants.borrow_status import BorrowStatus


class TestBorrow:
    """借用管理相关测试"""

    def test_create_borrow(self, client, user_token, test_asset):
        """测试普通用户提交借用申请"""
        response = client.post("/api/borrows", json={
            "asset_id": test_asset.id,
            "reason": "测试借用原因",
            "expected_return_date": "2099-12-31",
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["status"] == "pending"
        assert data["asset_id"] == test_asset.id

    def test_create_borrow_for_unavailable_asset(self, client, user_token, db, test_category):
        """测试对不可借用状态的资产提交申请失败"""
        from app.models.asset import Asset
        # 创建维修中状态的资产
        maintenance_asset = Asset(
            asset_number="MAINT-001",
            name="维修中资产",
            category_id=test_category.id,
            status=AssetStatus.MAINTENANCE,
        )
        db.add(maintenance_asset)
        db.commit()
        db.refresh(maintenance_asset)

        response = client.post("/api/borrows", json={
            "asset_id": maintenance_asset.id,
            "reason": "测试",
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 400

    def test_get_my_borrows(self, client, user_token, test_borrow):
        """测试用户获取自己的借用记录"""
        response = client.get("/api/borrows/my", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["total"] >= 1

    def test_get_all_borrows_as_admin(self, client, admin_token, test_borrow):
        """测试管理员获取所有借用记录"""
        response = client.get("/api/borrows", headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["total"] >= 1

    def test_get_all_borrows_as_user_forbidden(self, client, user_token):
        """测试普通用户无法获取所有借用记录"""
        response = client.get("/api/borrows", headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403

    def test_approve_borrow(self, client, admin_token, test_borrow, db):
        """测试管理员审批通过借用申请"""
        response = client.put(f"/api/borrows/{test_borrow.id}/approve", json={
            "comment": "同意借用"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["status"] == "approved"

        # 验证资产状态变为已借出
        from app.models.asset import Asset
        asset = db.query(Asset).filter(Asset.id == test_borrow.asset_id).first()
        assert asset.status == AssetStatus.BORROWED

    def test_reject_borrow(self, client, approver_token, test_borrow):
        """测试审批人拒绝借用申请"""
        response = client.put(f"/api/borrows/{test_borrow.id}/reject", json={
            "comment": "不符合借用条件"
        }, headers={"Authorization": f"Bearer {approver_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["status"] == "rejected"

    def test_approve_already_processed_borrow(self, client, admin_token, test_borrow, db):
        """测试对已处理的借用申请重复审批失败"""
        # 先批准
        client.put(f"/api/borrows/{test_borrow.id}/approve", json={},
                   headers={"Authorization": f"Bearer {admin_token}"})
        # 再次批准应失败
        response = client.put(f"/api/borrows/{test_borrow.id}/approve", json={},
                               headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 400

    def test_return_asset(self, client, admin_token, user_token, test_borrow, db):
        """测试归还资产"""
        # 先批准借用
        client.put(f"/api/borrows/{test_borrow.id}/approve", json={},
                   headers={"Authorization": f"Bearer {admin_token}"})

        # 归还资产
        response = client.put(f"/api/borrows/{test_borrow.id}/return", json={
            "comment": "已归还"
        }, headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["status"] == "returned"
        assert data["actual_return_date"] is not None

        # 验证资产状态变回闲置
        from app.models.asset import Asset
        asset = db.query(Asset).filter(Asset.id == test_borrow.asset_id).first()
        assert asset.status == AssetStatus.IDLE

    def test_return_unapproved_borrow_fails(self, client, user_token, test_borrow):
        """测试归还未批准的借用申请失败"""
        response = client.put(f"/api/borrows/{test_borrow.id}/return", json={},
                               headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 400

    def test_get_borrow_detail(self, client, admin_token, test_borrow):
        """测试获取借用详情"""
        response = client.get(f"/api/borrows/{test_borrow.id}",
                               headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["id"] == test_borrow.id

    def test_approve_borrow_as_user_forbidden(self, client, user_token, test_borrow):
        """测试普通用户无权审批借用"""
        response = client.put(f"/api/borrows/{test_borrow.id}/approve", json={},
                               headers={"Authorization": f"Bearer {user_token}"})
        assert response.status_code == 403
