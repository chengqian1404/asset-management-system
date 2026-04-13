# 自定义异常类定义
from fastapi import HTTPException, status


class AppException(HTTPException):
    """应用基础异常类"""
    def __init__(self, status_code: int, message: str, detail: str = None):
        super().__init__(status_code=status_code, detail={"message": message, "detail": detail})


class NotFoundError(AppException):
    """资源不存在异常"""
    def __init__(self, message: str = "资源不存在"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)


class PermissionError(AppException):
    """权限不足异常"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, message=message)


class AuthenticationError(AppException):
    """认证失败异常"""
    def __init__(self, message: str = "认证失败"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, message=message)


class ValidationError(AppException):
    """数据验证异常"""
    def __init__(self, message: str = "数据验证失败", detail: str = None):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, message=message, detail=detail)


class ConflictError(AppException):
    """数据冲突异常"""
    def __init__(self, message: str = "数据冲突"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, message=message)


class BusinessError(AppException):
    """业务逻辑异常"""
    def __init__(self, message: str = "业务处理失败"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message)
