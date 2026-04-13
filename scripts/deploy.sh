#!/bin/bash
# Docker部署脚本

echo "🚀 部署资产管理系统..."

cd docker

# 停止旧容器
docker-compose down

# 拉取最新镜像
docker-compose pull

# 启动服务
docker-compose up -d

echo "✅ 部署完成！"
echo "   访问地址: http://localhost"
echo "   API文档: http://localhost/api/docs"
