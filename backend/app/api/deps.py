"""依赖注入模块"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from ..database import get_db
from ..utils.security import decode_token
from ..models.user import User
from ..constants.messages import Messages

# HTTP Bearer认证
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Messages.UNAUTHORIZED,
    )
    try:
        payload = decode_token(credentials.credentials)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=Messages.USER_DISABLED
        )
    return user


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """验证管理员权限"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=Messages.FORBIDDEN
        )
    return current_user


def get_manager_or_admin(current_user: User = Depends(get_current_user)) -> User:
    """验证主管或管理员权限"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=Messages.FORBIDDEN
        )
    return current_user
