# 部署指南

## Docker 部署（推荐）

### 开发环境

```bash
docker-compose -f docker/docker-compose.yml up -d
```

### 生产环境

```bash
# 配置环境变量
export SECRET_KEY="your-production-secret-key"
export DEBUG=False

# 构建并启动
docker-compose -f docker/docker-compose.yml --profile production up -d
```

## 手动部署

### 后端部署

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 前端构建

```bash
cd frontend
npm run build
# dist/ 目录即为静态文件，部署到 Nginx
```

### Nginx 配置

参考 `docker/nginx.conf` 进行配置。

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| SECRET_KEY | (随机) | JWT密钥 |
| DATABASE_URL | sqlite:///./asset_management.db | 数据库地址 |
| DEBUG | True | 调试模式 |
| CORS_ORIGINS | localhost:3000 | 允许的来源 |
