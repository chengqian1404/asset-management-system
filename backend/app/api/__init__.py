# API模块初始化，汇集所有路由
from fastapi import APIRouter
from app.api import auth, asset, category, borrow, user, report, system

# 创建主API路由器
api_router = APIRouter(prefix="/api")

# 注册各模块路由
api_router.include_router(auth.router)
api_router.include_router(asset.router)
api_router.include_router(category.router)
api_router.include_router(borrow.router)
api_router.include_router(user.router)
api_router.include_router(report.router)
api_router.include_router(system.router)
