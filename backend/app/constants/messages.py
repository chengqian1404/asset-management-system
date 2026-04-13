# 系统消息常量定义（中文）

class Messages:
    # 认证相关消息
    LOGIN_SUCCESS = "登录成功"
    LOGIN_FAILED = "用户名或密码错误"
    LOGOUT_SUCCESS = "退出登录成功"
    TOKEN_EXPIRED = "令牌已过期"
    TOKEN_INVALID = "令牌无效"
    NOT_AUTHENTICATED = "未认证，请先登录"
    PERMISSION_DENIED = "权限不足"

    # 用户相关消息
    USER_CREATED = "用户创建成功"
    USER_UPDATED = "用户更新成功"
    USER_DELETED = "用户删除成功"
    USER_NOT_FOUND = "用户不存在"
    USER_ALREADY_EXISTS = "用户名或邮箱已存在"
    CANNOT_DELETE_SELF = "不能删除自己的账号"
    CANNOT_DELETE_ADMIN = "不能删除管理员账号"

    # 资产相关消息
    ASSET_CREATED = "资产创建成功"
    ASSET_UPDATED = "资产更新成功"
    ASSET_DELETED = "资产删除成功"
    ASSET_NOT_FOUND = "资产不存在"
    ASSET_NUMBER_EXISTS = "资产编号已存在"
    ASSET_CANNOT_BORROW = "该资产当前状态不可借用"
    ASSET_IMPORT_SUCCESS = "资产导入成功"

    # 分类相关消息
    CATEGORY_CREATED = "分类创建成功"
    CATEGORY_UPDATED = "分类更新成功"
    CATEGORY_DELETED = "分类删除成功"
    CATEGORY_NOT_FOUND = "分类不存在"
    CATEGORY_HAS_ASSETS = "该分类下存在资产，无法删除"

    # 借用相关消息
    BORROW_CREATED = "借用申请提交成功"
    BORROW_APPROVED = "借用申请已批准"
    BORROW_REJECTED = "借用申请已拒绝"
    BORROW_RETURNED = "资产归还成功"
    BORROW_NOT_FOUND = "借用记录不存在"
    BORROW_ALREADY_PROCESSED = "借用申请已处理"
    BORROW_NOT_APPROVED = "借用申请未批准，无法归还"

    # 系统相关消息
    SETTINGS_UPDATED = "系统设置更新成功"
    BACKUP_SUCCESS = "数据库备份成功"
    RESTORE_SUCCESS = "数据库恢复成功"
    OPERATION_SUCCESS = "操作成功"
    OPERATION_FAILED = "操作失败"
