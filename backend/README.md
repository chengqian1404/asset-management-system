# 资产管理系统后端

基于Python FastAPI构建的资产管理系统后端API。

## 技术栈

- **框架**: FastAPI 0.109.0
- **ORM**: SQLAlchemy 2.0 (同步模式)
- **数据验证**: Pydantic v2
- **认证**: JWT (HS256, 访问令牌30分钟, 刷新令牌7天)
- **数据库**: SQLite + Alembic迁移
- **测试**: Pytest + TestClient

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python scripts/init_db.py
```

### 3. 启动服务

```bash
uvicorn app.main:app --reload
```

服务默认运行在 http://localhost:8000

API文档: http://localhost:8000/docs

## 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 审批人 | approver | approver123 |
| 普通用户 | user1~user3 | user123 |

## API接口

### 认证
- `POST /api/auth/login` - 登录
- `POST /api/auth/refresh` - 刷新令牌
- `GET /api/auth/me` - 获取当前用户
- `POST /api/auth/logout` - 退出登录

### 资产管理
- `GET /api/assets` - 获取资产列表（分页、搜索、筛选）
- `POST /api/assets` - 创建资产
- `GET /api/assets/stats` - 资产统计
- `GET /api/assets/{id}` - 资产详情
- `PUT /api/assets/{id}` - 更新资产
- `DELETE /api/assets/{id}` - 删除资产
- `POST /api/assets/import` - Excel批量导入

### 分类管理
- `GET /api/categories` - 分类列表
- `POST /api/categories` - 创建分类
- `PUT /api/categories/{id}` - 更新分类
- `DELETE /api/categories/{id}` - 删除分类

### 借用管理
- `GET /api/borrows` - 借用记录列表（管理员/审批人）
- `POST /api/borrows` - 提交借用申请
- `GET /api/borrows/my` - 我的借用记录
- `PUT /api/borrows/{id}/approve` - 审批通过
- `PUT /api/borrows/{id}/reject` - 拒绝申请
- `PUT /api/borrows/{id}/return` - 归还资产
- `GET /api/borrows/{id}` - 借用详情

### 用户管理
- `GET /api/users` - 用户列表
- `POST /api/users` - 创建用户
- `PUT /api/users/{id}` - 更新用户
- `DELETE /api/users/{id}` - 删除用户
- `GET /api/users/{id}/permissions` - 用户权限

### 统计报告
- `GET /api/reports/asset-stats` - 资产统计报告
- `GET /api/reports/borrow-stats` - 借用统计报告
- `GET /api/reports/category-stats` - 分类统计报告

### 系统管理
- `GET /api/system/health` - 健康检查
- `GET /api/system/settings` - 系统设置
- `PUT /api/system/settings` - 更新设置
- `POST /api/system/backup` - 备份数据库
- `POST /api/system/restore` - 恢复数据库
- `GET /api/system/logs` - 操作日志

## 权限说明

- **admin（管理员）**: 全部权限，包括用户管理和系统设置
- **approver（审批人）**: 可审批借用申请，管理资产
- **user（普通用户）**: 可查看资产，提交借用申请

## 运行测试

```bash
cd backend
pytest tests/ -v
```

## Docker部署

```bash
cd backend
docker-compose up -d
```
