#!/bin/bash
# 开发环境启动脚本

echo "🚀 启动资产管理系统开发环境..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未找到Node.js，请先安装"
    exit 1
fi

# 启动后端
echo "📦 启动后端服务..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt -q
python scripts/init_db.py
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
echo "✅ 后端已启动 (PID: $BACKEND_PID) - http://localhost:8000"

# 启动前端
echo "🎨 启动前端服务..."
cd ../frontend
npm install --legacy-peer-deps -q
npm run dev &
FRONTEND_PID=$!
echo "✅ 前端已启动 (PID: $FRONTEND_PID) - http://localhost:5173"

echo ""
echo "🎉 系统已启动！"
echo "   前端: http://localhost:5173"
echo "   后端: http://localhost:8000"
echo "   API文档: http://localhost:8000/api/docs"
echo "   默认账号: admin / admin123"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待中断信号
trap "kill $BACKEND_PID $FRONTEND_PID" SIGINT SIGTERM
wait
