from typing import List
from pydantic_settings import BaseSettings
from pydantic import EmailStr, validator
import secrets
import logging
import warnings
import os

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Settings(BaseSettings):
    # 应用配置
    PROJECT_NAME: str = "个性化食谱管理系统"
    VERSION: str = "1.0.0"
    
    # 安全配置
    SECRET_KEY: str = secrets.token_urlsafe(32)  # 生成安全的随机密钥
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 延长token过期时间为24小时
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 添加刷新token功能，有效期7天
    REVOKE_EXISTING_TOKENS_ON_LOGIN: bool = True  # 登录时是否撤销现有的令牌
    MAX_LOGIN_ATTEMPTS: int = 5  # 最大登录尝试次数
    
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
            logger.warning("SECRET_KEY is too short. Setting a stronger SECRET_KEY is recommended.")
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @validator("ALGORITHM")
    def algorithm_must_be_supported(cls, v: str) -> str:
        """
        验证ALGORITHM必须是支持的算法
        """
        supported_algorithms = ["HS256", "HS512", "RS256"]
        if v not in supported_algorithms:
            error_msg = f"不支持的算法 {v}。支持的算法有: {supported_algorithms}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        return v
    
    @validator("PASSWORD_MIN_LENGTH")
    def password_min_length_must_be_positive(cls, v: int) -> int:
        """
        验证密码最小长度必须为正数
        """
        if v <= 0:
            error_msg = f"密码最小长度必须为正数，当前值: {v}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        return v
    
    @validator("RATE_LIMIT_PER_MINUTE")
    def rate_limit_must_be_positive(cls, v: int) -> int:
        """
        验证限流配置必须为正数
        """
        if v <= 0:
            error_msg = f"限流配置必须为正数，当前值: {v}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # 允许额外的环境变量
        env_file_encoding = 'utf-8'

# 创建全局配置实例
try:
    settings = Settings()
    logger.info(f"应用配置加载成功，项目名称: {settings.PROJECT_NAME}")
    
    # 检查环境变量文件是否存在
    if not os.path.exists(".env"):
        logger.warning(".env文件未找到，使用默认配置")
    
    # 记录关键配置信息（屏蔽敏感信息）
    logger.info(f"版本: {settings.VERSION}")
    logger.info(f"访问令牌过期时间: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} 分钟")
    logger.info(f"刷新令牌过期时间: {settings.REFRESH_TOKEN_EXPIRE_DAYS} 天")
    logger.info(f"算法: {settings.ALGORITHM}")
    logger.info(f"数据库架构: {settings.DATABASE_SCHEMA}")
    logger.info(f"CORS源: {settings.BACKEND_CORS_ORIGINS}")
    logger.info(f"是否使用PgBouncer: {settings.USE_PGBOUNCER}")
    logger.info(f"限流配置: {settings.RATE_LIMIT_PER_MINUTE} 次/分钟")
    
    # 屏蔽敏感信息后的数据库URL日志
    if hasattr(settings, 'DATABASE_URL'):
        import re
        masked_db_url = re.sub(r':(.*?)@', ':******@', settings.DATABASE_URL)
        logger.info(f"数据库URL (已屏蔽密码): {masked_db_url}")
    
    if hasattr(settings, 'PGBOUNCER_URL'):
        import re
        masked_pgbouncer_url = re.sub(r':(.*?)@', ':******@', settings.PGBOUNCER_URL)
        logger.info(f"PgBouncer URL (已屏蔽密码): {masked_pgbouncer_url}")
    
    # 密码策略日志
    logger.info(f"密码策略 - 最小长度: {settings.PASSWORD_MIN_LENGTH}")
    logger.info(f"密码策略 - 需要大写字母: {settings.PASSWORD_REQUIRE_UPPERCASE}")
    logger.info(f"密码策略 - 需要小写字母: {settings.PASSWORD_REQUIRE_LOWERCASE}")
    logger.info(f"密码策略 - 需要数字: {settings.PASSWORD_REQUIRE_DIGIT}")
    logger.info(f"密码策略 - 需要特殊字符: {settings.PASSWORD_REQUIRE_SPECIAL}")
    
    # 安全配置日志
    logger.info(f"最大登录尝试次数: {settings.MAX_LOGIN_ATTEMPTS}")
    logger.info(f"登录时撤销现有令牌: {settings.REVOKE_EXISTING_TOKENS_ON_LOGIN}")
    logger.info(f"安全HTTP头配置: {settings.SECURE_HTTP_HEADERS}")
    
except Exception as e:
    logger.critical(f"应用配置加载失败: {str(e)}")
    logger.critical(f"错误详情: {e.__class__.__name__}")
    raise Exception(f"初始化应用配置失败: {str(e)}")
