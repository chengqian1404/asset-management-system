# 用户相关Schema定义
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from app.constants.role import UserRole


class UserBase(BaseModel):
    """用户基础字段"""
    username: str
    email: str
    full_name: str
    department: Optional[str] = None
    role: UserRole = UserRole.USER
    is_active: bool = True


class UserCreate(UserBase):
    """创建用户请求"""
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """验证密码强度"""
        if len(v) < 6:
            raise ValueError("密码长度不能少于6位")
        return v


class UserUpdate(BaseModel):
    """更新用户请求"""
    email: Optional[str] = None
    full_name: Optional[str] = None
    department: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class UserResponse(UserBase):
    """用户响应数据"""
    id: int
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserPermissions(BaseModel):
    """用户权限信息"""
    can_manage_users: bool = False      # 可以管理用户
    can_approve_borrows: bool = False   # 可以审批借用
    can_manage_assets: bool = False     # 可以管理资产
    can_manage_system: bool = False     # 可以管理系统设置
    can_export_reports: bool = False    # 可以导出报告
