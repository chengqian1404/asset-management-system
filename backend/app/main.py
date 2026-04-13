"""FastAPI 应用入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import create_tables
from .api import auth, asset, category, borrow, user, report, system

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="中文版资产管理系统 API 文档",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(asset.router, prefix="/api/assets", tags=["资产管理"])
app.include_router(category.router, prefix="/api/categories", tags=["分类管理"])
app.include_router(borrow.router, prefix="/api/borrows", tags=["借用管理"])
app.include_router(user.router, prefix="/api/users", tags=["用户管理"])
app.include_router(report.router, prefix="/api/reports", tags=["报表"])
app.include_router(system.router, prefix="/api/system", tags=["系统"])


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    create_tables()


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok", "version": settings.APP_VERSION}
