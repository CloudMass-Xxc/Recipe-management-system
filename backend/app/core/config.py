from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    # 应用配置
    PROJECT_NAME: str = "个性化食谱管理系统"
    VERSION: str = "1.0.0"
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-here-please-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 数据库配置
    DATABASE_URL: str
    DATABASE_SCHEMA: str = "app_schema"
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    
    # AI服务配置 (主要配置在app/ai_service/config.py中)
    
    # PgBouncer配置
    USE_PGBOUNCER: bool = False
    PGBOUNCER_URL: str = "postgresql://app_user:app_password@localhost:6432/recipe_system"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # 允许额外的环境变量

# 创建全局配置实例
settings = Settings()