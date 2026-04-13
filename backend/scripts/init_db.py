#!/usr/bin/env python3
"""
数据库初始化脚本
运行方式: python scripts/init_db.py（从backend目录）
创建所有表并初始化示例数据
"""
import sys
import os
from datetime import date, timedelta

# 将backend目录加入Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, SessionLocal, create_tables
from app.models.base import Base
from app.models.user import User
from app.models.category import Category
from app.models.asset import Asset
from app.models.borrow import Borrow
from app.utils.security import hash_password
from app.constants.role import UserRole
from app.constants.status import AssetStatus
from app.constants.borrow_status import BorrowStatus


def init_database():
    """初始化数据库：创建表并插入示例数据"""
    print("=== 开始初始化数据库 ===")

    # 创建所有表
    create_tables()
    print("✓ 数据库表创建完成")

    db = SessionLocal()
    try:
        # 检查是否已有数据
        if db.query(User).count() > 0:
            print("✓ 数据库已有数据，跳过初始化")
            return

        # ===== 创建用户 =====
        print("正在创建用户...")

        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=hash_password("admin123"),
            full_name="系统管理员",
            department="信息技术部",
            role=UserRole.ADMIN,
            is_active=True,
        )
        approver = User(
            username="approver",
            email="approver@example.com",
            password_hash=hash_password("approver123"),
            full_name="张审批",
            department="行政部",
            role=UserRole.APPROVER,
            is_active=True,
        )
        user1 = User(
            username="user1",
            email="user1@example.com",
            password_hash=hash_password("user123"),
            full_name="李小明",
            department="技术部",
            role=UserRole.USER,
            is_active=True,
        )
        user2 = User(
            username="user2",
            email="user2@example.com",
            password_hash=hash_password("user123"),
            full_name="王小红",
            department="市场部",
            role=UserRole.USER,
            is_active=True,
        )
        user3 = User(
            username="user3",
            email="user3@example.com",
            password_hash=hash_password("user123"),
            full_name="陈小华",
            department="财务部",
            role=UserRole.USER,
            is_active=True,
        )

        db.add_all([admin, approver, user1, user2, user3])
        db.flush()  # 获取ID
        print(f"  ✓ 创建了 5 个用户")

        # ===== 创建资产分类 =====
        print("正在创建资产分类...")

        categories = [
            Category(name="电脑设备", description="台式机、笔记本、服务器等计算机设备", icon="computer"),
            Category(name="办公家具", description="桌椅、文件柜、储物柜等办公家具", icon="chair"),
            Category(name="网络设备", description="路由器、交换机、防火墙等网络设备", icon="router"),
            Category(name="打印设备", description="打印机、复印机、扫描仪等设备", icon="print"),
            Category(name="其他设备", description="投影仪、会议设备等其他办公设备", icon="device"),
        ]
        db.add_all(categories)
        db.flush()
        cat_map = {c.name: c for c in categories}
        print(f"  ✓ 创建了 5 个资产分类")

        # ===== 创建资产 =====
        print("正在创建资产...")

        assets_data = [
            # 电脑设备
            ("PC-001", "联想ThinkPad X1 Carbon笔记本", "电脑设备", AssetStatus.IN_USE, "技术部201", admin.id, "联想"),
            ("PC-002", "戴尔Latitude 5520笔记本", "电脑设备", AssetStatus.IN_USE, "市场部301", user2.id, "戴尔"),
            ("PC-003", "苹果MacBook Pro 14寸", "电脑设备", AssetStatus.IDLE, "IT仓库", None, "苹果"),
            ("PC-004", "惠普EliteBook 840笔记本", "电脑设备", AssetStatus.MAINTENANCE, "维修室", None, "惠普"),
            ("SRV-001", "戴尔PowerEdge R740服务器", "电脑设备", AssetStatus.IN_USE, "机房", admin.id, "戴尔"),
            # 办公家具
            ("FURN-001", "宜家MARKUS人体工学椅", "办公家具", AssetStatus.IN_USE, "技术部201", user1.id, "宜家"),
            ("FURN-002", "西昊M57办公椅", "办公家具", AssetStatus.IDLE, "仓库", None, "西昊"),
            ("FURN-003", "乐歌电动升降桌", "办公家具", AssetStatus.IN_USE, "市场部301", user2.id, "乐歌"),
            # 网络设备
            ("NET-001", "思科Catalyst 2960交换机", "网络设备", AssetStatus.IN_USE, "机房", admin.id, "思科"),
            ("NET-002", "华为AR6280路由器", "网络设备", AssetStatus.IN_USE, "机房", admin.id, "华为"),
            ("NET-003", "TP-LINK TL-SG1024D交换机", "网络设备", AssetStatus.IDLE, "IT仓库", None, "TP-LINK"),
            # 打印设备
            ("PRT-001", "惠普LaserJet Pro M404dn打印机", "打印设备", AssetStatus.IN_USE, "行政部101", approver.id, "惠普"),
            ("PRT-002", "爱普生WF-C5810复合机", "打印设备", AssetStatus.IN_USE, "财务部401", user3.id, "爱普生"),
            ("PRT-003", "佳能imageCLASS MF445dw", "打印设备", AssetStatus.SCRAPPED, "废品区", None, "佳能"),
            # 其他设备
            ("PROJ-001", "爱普生CB-X05E投影仪", "其他设备", AssetStatus.IDLE, "会议室A", None, "爱普生"),
            ("PROJ-002", "明基MS506H投影仪", "其他设备", AssetStatus.IN_USE, "会议室B", None, "明基"),
            ("CAM-001", "海康威视DS-2CD2T47摄像头", "其他设备", AssetStatus.IN_USE, "大厅", admin.id, "海康威视"),
            ("UPS-001", "山特C6KS UPS电源", "其他设备", AssetStatus.IN_USE, "机房", admin.id, "山特"),
            ("TEL-001", "思科IP Phone 7942G电话机", "其他设备", AssetStatus.IN_USE, "前台", None, "思科"),
            ("TEL-002", "先锋数码录音笔", "其他设备", AssetStatus.IDLE, "行政仓库", None, "先锋"),
        ]

        asset_objects = []
        for i, (number, name, cat_name, status, location, owner_id, supplier) in enumerate(assets_data):
            asset = Asset(
                asset_number=number,
                name=name,
                category_id=cat_map[cat_name].id,
                status=status,
                location=location,
                owner_id=owner_id,
                purchase_date=date.today() - timedelta(days=365 * (i % 3 + 1)),
                purchase_price=round(1000 + i * 500, 2),
                supplier=supplier,
                description=f"{name}，{supplier}品牌产品",
            )
            asset_objects.append(asset)

        db.add_all(asset_objects)
        db.flush()
        print(f"  ✓ 创建了 {len(asset_objects)} 个资产")

        # ===== 创建借用记录 =====
        print("正在创建借用记录...")

        # 找到闲置资产用于借用
        idle_assets = [a for a in asset_objects if a.status == AssetStatus.IDLE]

        borrows = [
            Borrow(
                asset_id=idle_assets[0].id,
                user_id=user1.id,
                approver_id=approver.id,
                status=BorrowStatus.APPROVED,
                reason="项目开发需要",
                expected_return_date=date.today() + timedelta(days=7),
            ),
            Borrow(
                asset_id=idle_assets[1].id if len(idle_assets) > 1 else idle_assets[0].id,
                user_id=user2.id,
                status=BorrowStatus.PENDING,
                reason="出差使用",
                expected_return_date=date.today() + timedelta(days=3),
            ),
            Borrow(
                asset_id=asset_objects[0].id,
                user_id=user3.id,
                approver_id=approver.id,
                status=BorrowStatus.RETURNED,
                reason="培训使用",
                expected_return_date=date.today() - timedelta(days=10),
                actual_return_date=date.today() - timedelta(days=12),
            ),
            Borrow(
                asset_id=asset_objects[1].id,
                user_id=user1.id,
                approver_id=admin.id,
                status=BorrowStatus.REJECTED,
                reason="测试用途",
                expected_return_date=date.today() + timedelta(days=5),
            ),
            Borrow(
                asset_id=asset_objects[4].id,
                user_id=user2.id,
                approver_id=approver.id,
                status=BorrowStatus.OVERDUE,
                reason="长期项目使用",
                expected_return_date=date.today() - timedelta(days=5),
            ),
        ]

        db.add_all(borrows)
        print(f"  ✓ 创建了 {len(borrows)} 条借用记录")

        db.commit()
        print("\n=== 数据库初始化完成 ===")
        print(f"管理员账号: admin / admin123")
        print(f"审批人账号: approver / approver123")
        print(f"普通用户账号: user1~user3 / user123")

    except Exception as e:
        db.rollback()
        print(f"\n✗ 初始化失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
