#!/usr/bin/env python3
"""
创建管理员账号脚本
运行方式: python scripts/create_admin.py（从backend目录）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, create_tables
from app.models.user import User
from app.utils.security import hash_password
from app.constants.role import UserRole


def create_admin(username: str, password: str, email: str, full_name: str):
    """创建管理员账号"""
    create_tables()
    db = SessionLocal()
    try:
        # 检查用户名是否已存在
        if db.query(User).filter(User.username == username).first():
            print(f"✗ 用户名 {username} 已存在")
            return

        admin = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            full_name=full_name,
            department="系统管理",
            role=UserRole.ADMIN,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print(f"✓ 管理员账号创建成功: {username}")
    finally:
        db.close()


if __name__ == "__main__":
    # 可通过命令行参数自定义，默认创建示例管理员
    username = sys.argv[1] if len(sys.argv) > 1 else "admin"
    password = sys.argv[2] if len(sys.argv) > 2 else "admin123"
    email = sys.argv[3] if len(sys.argv) > 3 else "admin@example.com"
    full_name = sys.argv[4] if len(sys.argv) > 4 else "系统管理员"

    create_admin(username, password, email, full_name)
