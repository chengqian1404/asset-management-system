"""消息常量"""


class Messages:
    # 通用消息
    SUCCESS = "操作成功"
    FAILED = "操作失败"
    NOT_FOUND = "记录不存在"
    UNAUTHORIZED = "未授权访问"
    FORBIDDEN = "权限不足"

    # 认证消息
    LOGIN_SUCCESS = "登录成功"
    LOGIN_FAILED = "用户名或密码错误"
    TOKEN_EXPIRED = "Token已过期"
    TOKEN_INVALID = "Token无效"

    # 用户消息
    USER_NOT_FOUND = "用户不存在"
    USER_EXISTS = "用户名已存在"
    EMAIL_EXISTS = "邮箱已存在"
    USER_DISABLED = "用户已被禁用"

    # 资产消息
    ASSET_NOT_FOUND = "资产不存在"
    ASSET_NUMBER_EXISTS = "资产编号已存在"
    ASSET_IN_USE = "资产正在使用中"

    # 借用消息
    BORROW_NOT_FOUND = "借用记录不存在"
    BORROW_ASSET_UNAVAILABLE = "资产不可借用"
    BORROW_ALREADY_RETURNED = "资产已归还"
