from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import logging
import traceback
import time

from app.core.config import settings
from app.core.database import init_database, create_tables
from app.core.exceptions import APIException
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.recipes.routes import router as recipes_router
from app.ai_service.routes import router as ai_router

# 配置全局日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# 自定义异常处理类
class APIException(Exception):
    """
    API自定义异常类
    """
    def __init__(self, status_code: int, detail: str, error_type: str = "api_error"):
        self.status_code = status_code
        self.detail = detail
        self.error_type = error_type
        super().__init__(self.detail)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用程序生命周期管理
    
    Args:
        app: FastAPI应用实例
    """
    # 启动时的初始化操作
    try:
        logger.info("正在启动个性化食谱管理系统API...")
        
        # 初始化数据库连接
        init_database()
        
        # 创建数据库表
        create_tables()
        
        logger.info("数据库初始化完成")
        
        yield
        
    except Exception as e:
        logger.critical(f"应用程序启动失败: {str(e)}")
        logger.critical(f"错误堆栈: {traceback.format_exc()}")
        raise
    finally:
        # 关闭时的清理操作
        logger.info("正在关闭个性化食谱管理系统API...")


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI食谱推荐系统API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    """
    处理API自定义异常
    """
    logger.error(f"API异常 - {exc.error_type}: {exc.detail}, 路径: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"type": exc.error_type, "message": exc.detail}}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    处理HTTP异常
    """
    logger.error(f"HTTP异常 - 状态码: {exc.status_code}, 详情: {exc.detail}, 路径: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"type": "http_error", "message": exc.detail}}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    处理一般异常
    """
    logger.critical(f"未处理的异常 - {str(exc)}, 路径: {request.url.path}")
    logger.critical(f"错误堆栈: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"error": {"type": "server_error", "message": "服务器内部错误"}}
    )


# 请求中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    记录请求日志的中间件
    """
    # 请求开始时间
    start_time = time.time()
    
    # 记录请求信息
    client_ip = request.client.host
    logger.info(f"请求开始 - {request.method} {request.url.path}, IP: {client_ip}")
    
    try:
        # 处理请求
        response = await call_next(request)
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 记录响应信息
        logger.info(f"请求完成 - {request.method} {request.url.path}, 状态码: {response.status_code}, 处理时间: {process_time:.4f}s, IP: {client_ip}")
        
        # 添加处理时间到响应头
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
        
    except Exception as e:
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 记录异常信息
        logger.error(f"请求异常 - {request.method} {request.url.path}, 错误: {str(e)}, 处理时间: {process_time:.4f}s, IP: {client_ip}")
        
        # 重新抛出异常，让异常处理器处理
        raise


# 注册路由，添加/api前缀
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(recipes_router, prefix="/api")
app.include_router(ai_router, prefix="/api")

# 根路径
@app.get("/")
async def root():
    logger.info("根路径请求")
    return {"message": "Welcome to AI Recipe Recommendation System API"}

# 健康检查
@app.get("/health")
async def health_check():
    logger.info("健康检查请求")
    return {"status": "healthy", "version": settings.VERSION}

if __name__ == "__main__":
    try:
        logger.info(f"启动服务器 - 监听地址: 0.0.0.0:8002")
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8002,
            reload=False,  # 生产环境关闭热重载
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("服务器已停止 (用户中断)")
    except Exception as e:
        logger.critical(f"服务器启动失败: {str(e)}")
        logger.critical(f"错误堆栈: {traceback.format_exc()}")
        raise