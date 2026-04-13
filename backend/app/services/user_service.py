# 用户服务模块
from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserPermissions
from app.utils.security import hash_password
from app.utils.exceptions import NotFoundError, ConflictError, BusinessError
from app.constants.role import UserRole


class UserService:
    """用户管理服务类"""

    @staticmethod
    def get_users(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        role: Optional[str] = None,
    ) -> Tuple[int, List[User]]:
        """分页获取用户列表"""
        query = db.query(User)

        if search:
            query = query.filter(
                (User.username.ilike(f"%{search}%")) |
                (User.full_name.ilike(f"%{search}%")) |
                (User.email.ilike(f"%{search}%"))
            )
        if role:
            query = query.filter(User.role == role)

        total = query.count()
        users = query.order_by(User.created_at.desc()) \
                     .offset((page - 1) * page_size) \
                     .limit(page_size) \
                     .all()
        return total, users

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """根据ID获取用户"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError("用户不存在")
        return user

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """创建新用户"""
        # 检查用户名是否已存在
        if db.query(User).filter(User.username == user_data.username).first():
            raise ConflictError("用户名已存在")
        # 检查邮箱是否已存在
        if db.query(User).filter(User.email == user_data.email).first():
            raise ConflictError("邮箱已存在")

        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            full_name=user_data.full_name,
            department=user_data.department,
            role=user_data.role,
            is_active=user_data.is_active,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        """更新用户信息"""
        user = UserService.get_user(db, user_id)

        # 检查邮箱唯一性
        if user_data.email and user_data.email != user.email:
            if db.query(User).filter(User.email == user_data.email, User.id != user_id).first():
                raise ConflictError("邮箱已被其他用户使用")

        update_data = user_data.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["password_hash"] = hash_password(update_data.pop("password"))
        else:
            update_data.pop("password", None)

        for field, value in update_data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int, current_user_id: int) -> None:
        """删除用户"""
        if user_id == current_user_id:
            raise BusinessError("不能删除自己的账号")

        user = UserService.get_user(db, user_id)
        if user.role == UserRole.ADMIN:
            # 检查是否是唯一管理员
            admin_count = db.query(User).filter(User.role == UserRole.ADMIN).count()
            if admin_count <= 1:
                raise BusinessError("不能删除唯一的管理员账号")

        db.delete(user)
        db.commit()

    @staticmethod
    def get_permissions(user: User) -> UserPermissions:
        """根据用户角色获取权限列表"""
        if user.role == UserRole.ADMIN:
            return UserPermissions(
                can_manage_users=True,
                can_approve_borrows=True,
                can_manage_assets=True,
                can_manage_system=True,
                can_export_reports=True,
            )
        elif user.role == UserRole.APPROVER:
            return UserPermissions(
                can_manage_users=False,
                can_approve_borrows=True,
                can_manage_assets=True,
                can_manage_system=False,
                can_export_reports=True,
            )
        else:
            return UserPermissions(
                can_manage_users=False,
                can_approve_borrows=False,
                can_manage_assets=False,
                can_manage_system=False,
                can_export_reports=False,
            )
