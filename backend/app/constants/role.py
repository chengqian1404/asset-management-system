"""角色常量"""


class UserRole:
    ADMIN = "admin"      # 管理员
    MANAGER = "manager"  # 主管
    USER = "user"        # 普通用户


ROLE_LABELS = {
    UserRole.ADMIN: "管理员",
    UserRole.MANAGER: "主管",
    UserRole.USER: "普通用户",
}

# 权限配置
ROLE_PERMISSIONS = {
    UserRole.ADMIN: ["*"],  # 管理员拥有所有权限
    UserRole.MANAGER: [
        "asset:read", "asset:write",
        "borrow:read", "borrow:approve",
        "user:read",
        "report:read",
    ],
    UserRole.USER: [
        "asset:read",
        "borrow:read", "borrow:create",
    ],
}
