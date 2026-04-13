# 中间件模块 - 请求日志、CORS等
import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("asset_management.middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件，记录每个HTTP请求的基本信息"""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()

        # 记录请求信息
        logger.info(f"请求: {request.method} {request.url.path}")

        response = await call_next(request)

        # 计算处理时间
        process_time = (time.time() - start_time) * 1000
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

        logger.info(
            f"响应: {request.method} {request.url.path} "
            f"状态码={response.status_code} "
            f"耗时={process_time:.2f}ms"
        )
        return response
