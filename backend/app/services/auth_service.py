# 认证服务模块
from datetime import datetime, timezone
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.utils.exceptions import AuthenticationError
from app.config import settings


class AuthService:
    """认证服务类"""

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """验证用户凭证，返回用户对象或None"""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        if not user.is_active:
            return None
        return user

    @staticmethod
    def login(db: Session, login_data: LoginRequest) -> Tuple[User, TokenResponse]:
        """处理用户登录，返回用户和令牌"""
        user = AuthService.authenticate_user(db, login_data.username, login_data.password)
        if not user:
            raise AuthenticationError("用户名或密码错误")

        # 更新最后登录时间
        user.last_login = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)

        # 生成令牌
        token_data = {"sub": str(user.id), "username": user.username}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        token_response = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return user, token_response

    @staticmethod
    def refresh_token(refresh_token: str) -> TokenResponse:
        """使用刷新令牌获取新的访问令牌"""
        payload = decode_token(refresh_token)
        if not payload:
            raise AuthenticationError("刷新令牌无效或已过期")

        # 验证令牌类型
        if payload.get("type") != "refresh":
            raise AuthenticationError("令牌类型错误")

        # 生成新的令牌对
        token_data = {"sub": payload.get("sub"), "username": payload.get("username")}
        new_access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    @staticmethod
    def get_current_user(db: Session, token: str) -> User:
        """从令牌获取当前用户"""
        payload = decode_token(token)
        if not payload:
            raise AuthenticationError("令牌无效或已过期")

        if payload.get("type") != "access":
            raise AuthenticationError("令牌类型错误")

        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("令牌数据无效")

        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise AuthenticationError("用户不存在")
        if not user.is_active:
            raise AuthenticationError("用户账号已禁用")

        return user
