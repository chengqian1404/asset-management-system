# 开发指南

## 开发环境搭建

```bash
bash scripts/dev.sh
```

## 后端开发

### 新增API接口

1. 在 `backend/app/api/` 创建路由文件
2. 在 `backend/app/services/` 实现业务逻辑
3. 在 `backend/app/schemas/` 定义数据格式
4. 在 `backend/app/main.py` 注册路由

### 数据库迁移

```bash
cd backend
alembic revision --autogenerate -m "描述"
alembic upgrade head
```

### 运行测试

```bash
cd backend
pytest tests/ -v
```

## 前端开发

### 新增页面

1. 在 `frontend/src/pages/` 创建Vue文件
2. 在 `frontend/src/router/index.js` 添加路由
3. 在 `frontend/src/api/` 添加API调用
4. 在 `frontend/src/components/common/Sidebar.vue` 添加菜单项

### 状态管理

使用Pinia进行状态管理：

```javascript
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()
```

## 代码规范

- 所有注释使用中文
- Python 函数需要 docstring
- Vue 组件使用 Composition API
