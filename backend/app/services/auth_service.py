"""认证服务"""
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.auth import RegisterRequest, TokenResponse
from ..utils.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)
from ..constants.messages import Messages
from ..config import settings


class AuthService:
    """认证业务逻辑"""

    def __init__(self, db: Session):
        self.db = db

    def login(self, username: str, password: str) -> TokenResponse:
        """用户登录"""
        user = self.db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=Messages.LOGIN_FAILED
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=Messages.USER_DISABLED
            )

        access_token = create_access_token({"sub": user.username})
        refresh_token = create_refresh_token({"sub": user.username})

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )

    def refresh_token(self, refresh_token: str) -> TokenResponse:
        """刷新Token"""
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=Messages.TOKEN_INVALID
                )
            username = payload.get("sub")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=Messages.TOKEN_INVALID
            )

        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=Messages.USER_NOT_FOUND
            )

        access_token = create_access_token({"sub": user.username})
        new_refresh_token = create_refresh_token({"sub": user.username})

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token
        )

    def register(self, request: RegisterRequest) -> User:
        """用户注册"""
        if self.db.query(User).filter(User.username == request.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Messages.USER_EXISTS
            )
        if self.db.query(User).filter(User.email == request.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Messages.EMAIL_EXISTS
            )

        user = User(
            username=request.username,
            email=request.email,
            password_hash=hash_password(request.password),
            full_name=request.full_name,
            department=request.department,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
