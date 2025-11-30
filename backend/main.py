from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import engine, Base
from app.core.init_db import init_db
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.recipes.routes import router as recipes_router
from app.ai_service.routes import router as ai_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"正在启动个性化食谱管理系统API...")
    print("正在初始化数据库...")
    init_db(drop_existing=False)  # 不删除现有表，只创建缺少的表或列
    print("数据库初始化完成")
    yield
    # Shutdown
    print(f"正在关闭个性化食谱管理系统API...")

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

# 注册路由
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(recipes_router)
app.include_router(ai_router)

# 根路径
@app.get("/")
async def root():
    return {"message": "Welcome to AI Recipe Recommendation System API"}

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)