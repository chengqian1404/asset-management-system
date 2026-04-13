# API 文档

## 认证

所有API（除登录外）需要在请求头添加：
```
Authorization: Bearer <access_token>
```

## 接口列表

### 认证模块

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/login | 用户登录 |
| POST | /api/auth/refresh | 刷新Token |
| POST | /api/auth/register | 用户注册 |
| GET | /api/auth/me | 获取当前用户 |

### 资产管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/assets | 资产列表（分页、搜索） |
| POST | /api/assets | 新增资产 |
| GET | /api/assets/{id} | 资产详情 |
| PUT | /api/assets/{id} | 更新资产 |
| DELETE | /api/assets/{id} | 删除资产 |
| GET | /api/assets/stats | 资产统计 |
| POST | /api/assets/import | 批量导入 |

### 借用管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/borrows | 借用列表 |
| POST | /api/borrows | 申请借用 |
| GET | /api/borrows/my | 我的借用 |
| PUT | /api/borrows/{id}/approve | 审批借用 |
| PUT | /api/borrows/{id}/return | 归还资产 |

## 响应格式

### 成功响应
```json
{
  "data": {...},
  "total": 100,
  "page": 1,
  "page_size": 20
}
```

### 错误响应
```json
{
  "detail": "错误信息"
}
```

## 完整API文档

启动后端服务后，访问 http://localhost:8000/api/docs 查看交互式API文档。
