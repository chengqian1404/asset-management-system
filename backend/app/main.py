# FastAPI应用主入口
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.config import settings
from app.database import create_tables
from app.api import api_router
from app.middleware import RequestLoggingMiddleware
from app.utils.exceptions import AppException

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="资产管理系统后端API - 提供资产、借用、用户管理等功能",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 添加CORS中间件，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加请求日志中间件
app.add_middleware(RequestLoggingMiddleware)


# 全局异常处理器 - 处理应用自定义异常
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """处理自定义应用异常，返回标准格式的错误响应"""
    detail = exc.detail if isinstance(exc.detail, dict) else {"message": str(exc.detail), "detail": None}
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": detail.get("message", "操作失败"),
            "detail": detail.get("detail"),
        }
    )


# 全局异常处理器 - 处理Pydantic验证错误
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理请求数据验证失败，返回友好的错误提示"""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append(f"{field}: {error['msg']}")

    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "message": "请求数据格式错误",
            "detail": "; ".join(errors),
        }
    )


# 注册API路由
app.include_router(api_router)


# 应用启动事件 - 初始化数据库表
@app.on_event("startup")
def startup_event():
    """应用启动时创建数据库表"""
    create_tables()


# 根路径健康检查
@app.get("/", summary="根路径")
def root():
    """根路径，返回应用基本信息"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "运行中",
        "docs": "/docs",
    }
