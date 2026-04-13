#!/bin/bash
# 构建脚本

echo "🔨 开始构建资产管理系统..."

# 构建前端
echo "📦 构建前端..."
cd frontend
npm install --legacy-peer-deps
npm run build
cd ..
echo "✅ 前端构建完成"

# 构建Docker镜像
echo "🐳 构建Docker镜像..."
docker build -f docker/Dockerfile.prod -t asset-management:latest .
echo "✅ Docker镜像构建完成"

echo "🎉 构建完成！"
