#!/bin/bash
# 测试脚本

echo "🧪 运行测试..."

# 后端测试
echo "🐍 运行后端测试..."
cd backend
pip install -r requirements.txt -q
pytest tests/ -v --tb=short
cd ..

echo "✅ 测试完成！"
