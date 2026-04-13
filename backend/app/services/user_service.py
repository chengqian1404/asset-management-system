"""用户业务逻辑"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..utils.security import hash_password
from ..constants.messages import Messages


class UserService:
    """用户管理业务逻辑"""

    def __init__(self, db: Session):
        self.db = db

    def list_users(self, page: int, page_size: int, keyword=None):
        """获取用户列表"""
        query = self.db.query(User)

        if keyword:
            query = query.filter(
                or_(
                    User.username.ilike(f"%{keyword}%"),
                    User.full_name.ilike(f"%{keyword}%"),
                    User.email.ilike(f"%{keyword}%"),
                )
            )

        total = query.count()
        users = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            "data": users,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def create_user(self, user_data: UserCreate) -> User:
        """创建用户"""
        if self.db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Messages.USER_EXISTS
            )
        if self.db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Messages.EMAIL_EXISTS
            )

        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            full_name=user_data.full_name,
            department=user_data.department,
            role=user_data.role,
            is_active=user_data.is_active,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """更新用户"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=Messages.USER_NOT_FOUND)

        update_data = user_data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = hash_password(update_data.pop("password"))

        for key, value in update_data.items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int):
        """删除用户"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=Messages.USER_NOT_FOUND)
        self.db.delete(user)
        self.db.commit()
