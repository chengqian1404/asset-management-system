# 📦 中文版资产管理系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.x-green.svg)](https://vuejs.org/)

> 轻量级、高可迭代的中文资产管理系统，基于 ERPNext 架构思想设计

## 🚀 快速开始

### 一键启动（Docker）

```bash
git clone https://github.com/your-org/asset-management-system.git
cd asset-management-system
docker-compose -f docker/docker-compose.yml up -d
```

访问 http://localhost:5173，使用 `admin / admin123` 登录。

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/your-org/asset-management-system.git
cd asset-management-system

# 启动开发环境
bash scripts/dev.sh
```

## 📋 功能特性

| 模块 | 功能 |
|------|------|
| 认证 | JWT登录、Token刷新、用户注册 |
| 资产管理 | 增删改查、批量导入、二维码生成 |
| 分类管理 | 资产分类的增删改查 |
| 借用管理 | 申请、审批、归还全流程 |
| 用户管理 | 多角色权限（管理员/主管/普通用户） |
| 报表统计 | 资产状态分布、借用统计 |
| 系统设置 | 操作日志、系统配置 |

## 🏗️ 技术栈

- **前端**：Vue 3 + Vite + Element Plus + Pinia
- **后端**：Python FastAPI + SQLAlchemy + JWT
- **数据库**：SQLite（开发） / PostgreSQL（生产）
- **部署**：Docker + Docker Compose + Nginx

## 📁 项目结构

```
asset-management-system/
├── frontend/          # Vue 3 前端
├── backend/           # FastAPI 后端
├── docker/            # Docker配置
├── docs/              # 文档
└── scripts/           # 脚本工具
```

## 🔑 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 普通用户 | zhang_san | user123 |

## 📖 详细文档

- [安装指南](INSTALLATION.md)
- [API 文档](API.md)
- [架构设计](ARCHITECTURE.md)
- [部署指南](DEPLOYMENT.md)
- [开发指南](DEVELOPMENT.md)

## 📄 许可证

[MIT License](../LICENSE)
