"""创建管理员账号脚本"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, create_tables
from app.models.user import User
from app.utils.security import hash_password


def create_admin(username: str, password: str, email: str):
    create_tables()
    db = SessionLocal()
    try:
        if db.query(User).filter(User.username == username).first():
            print(f"用户 {username} 已存在")
            return
        admin = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role="admin",
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print(f"✅ 管理员账号创建成功: {username}")
    finally:
        db.close()


if __name__ == "__main__":
    username = input("管理员用户名: ")
    password = input("管理员密码: ")
    email = input("管理员邮箱: ")
    create_admin(username, password, email)
