from typing import List
from pydantic_settings import BaseSettings
from pydantic import EmailStr, validator
import secrets

class Settings(BaseSettings):
    # 应用配置
    PROJECT_NAME: str = "个性化食谱管理系统"
    VERSION: str = "1.0.0"
    
    # 安全配置
    SECRET_KEY: str = secrets.token_urlsafe(32)  # 生成安全的随机密钥
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 延长token过期时间为24小时
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 添加刷新token功能，有效期7天
    
    # 密码策略配置
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGIT: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True
    
    # 数据库配置
    DATABASE_URL: str
    DATABASE_SCHEMA: str = "app_schema"
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://localhost:5175"]
    
    # AI服务配置 (主要配置在app/ai_service/config.py中)
    
    # PgBouncer配置
    USE_PGBOUNCER: bool = False
    PGBOUNCER_URL: str = "postgresql://app_user:app_password@localhost:6432/recipe_system"
    
    # 限流配置
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # 安全HTTP头配置
    SECURE_HTTP_HEADERS: bool = True
    
    @validator("SECRET_KEY", pre=True)
    def secret_key_must_be_strong(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # 允许额外的环境变量

# 创建全局配置实例
settings = Settings()