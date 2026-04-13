"""数据库初始化脚本（包含示例数据）"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, create_tables
from app.models.user import User
from app.models.category import Category
from app.models.asset import Asset
from app.utils.security import hash_password


def init_db():
    """初始化数据库并创建示例数据"""
    create_tables()
    db = SessionLocal()

    try:
        # 创建管理员用户
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@example.com",
                password_hash=hash_password("admin123"),
                full_name="系统管理员",
                department="IT部门",
                role="admin",
                is_active=True,
            )
            db.add(admin)
            print("✅ 创建管理员用户: admin/admin123")

        # 创建示例普通用户
        if not db.query(User).filter(User.username == "zhang_san").first():
            user = User(
                username="zhang_san",
                email="zhangsan@example.com",
                password_hash=hash_password("user123"),
                full_name="张三",
                department="研发部",
                role="user",
                is_active=True,
            )
            db.add(user)

        db.commit()

        # 创建示例分类
        categories_data = [
            {"name": "电子设备", "description": "电脑、显示器、服务器等", "icon": "el-icon-monitor"},
            {"name": "办公家具", "description": "桌椅、柜子等办公设施", "icon": "el-icon-office-building"},
            {"name": "网络设备", "description": "路由器、交换机、网线等", "icon": "el-icon-connection"},
            {"name": "交通工具", "description": "公司车辆等", "icon": "el-icon-van"},
        ]

        for cat_data in categories_data:
            if not db.query(Category).filter(Category.name == cat_data["name"]).first():
                db.add(Category(**cat_data))

        db.commit()

        # 创建示例资产
        category = db.query(Category).filter(Category.name == "电子设备").first()
        admin_user = db.query(User).filter(User.username == "admin").first()

        assets_data = [
            {"asset_number": "IT-2024-001", "name": "联想ThinkPad笔记本", "status": "in_use",
             "location": "A栋301室", "purchase_price": 8500},
            {"asset_number": "IT-2024-002", "name": "Dell显示器27寸", "status": "idle",
             "location": "仓库B区", "purchase_price": 2000},
            {"asset_number": "IT-2024-003", "name": "MacBook Pro 14寸", "status": "in_use",
             "location": "B栋201室", "purchase_price": 14999},
        ]

        for asset_data in assets_data:
            if not db.query(Asset).filter(Asset.asset_number == asset_data["asset_number"]).first():
                asset = Asset(
                    **asset_data,
                    category_id=category.id if category else None,
                    owner_id=admin_user.id if admin_user else None,
                )
                db.add(asset)

        db.commit()
        print("✅ 数据库初始化完成！示例数据已创建。")
        print("📋 默认账号:")
        print("   管理员: admin / admin123")
        print("   普通用户: zhang_san / user123")

    except Exception as e:
        db.rollback()
        print(f"❌ 初始化失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
