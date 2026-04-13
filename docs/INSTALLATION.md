# 安装指南

## 环境要求

| 组件 | 版本要求 |
|------|---------|
| Python | 3.11+ |
| Node.js | 18+ |
| Docker | 20+ (可选) |

## 方式一：Docker 一键启动（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/your-org/asset-management-system.git
cd asset-management-system

# 2. 启动服务
docker-compose -f docker/docker-compose.yml up -d

# 3. 初始化数据库（首次启动）
docker exec asset-backend python scripts/init_db.py

# 4. 访问系统
# 前端: http://localhost:5173
# API文档: http://localhost:8000/api/docs
```

## 方式二：本地开发环境

### 后端安装

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env

# 初始化数据库
python scripts/init_db.py

# 启动服务
uvicorn app.main:app --reload --port 8000
```

### 前端安装

```bash
cd frontend

# 安装依赖
npm install --legacy-peer-deps

# 配置环境变量
cp .env.example .env.local

# 启动开发服务
npm run dev
```

## 默认访问信息

- **前端地址**：http://localhost:5173
- **API文档**：http://localhost:8000/api/docs
- **管理员账号**：admin / admin123
