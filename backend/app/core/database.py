from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError, IntegrityError
import logging
import traceback
import time
from contextlib import contextmanager
from fastapi import HTTPException

from .config import settings
from .exceptions import APIException

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 数据库连接参数
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20
DB_POOL_TIMEOUT = 30
DB_POOL_RECYCLE = 1800  # 30分钟后回收连接

# 创建数据库引擎
engine = None
SessionLocal = None
Base = None

def init_database():
    """
    初始化数据库连接
    
    Raises:
        Exception: 数据库连接初始化失败时抛出
    """
    global engine, SessionLocal, Base
    
    try:
        # 创建数据库引擎
        logger.info(f"正在连接数据库...")
        if settings.USE_PGBOUNCER:
            db_url = settings.PGBOUNCER_URL
        else:
            db_url = settings.DATABASE_URL
        
        engine = create_engine(
            db_url,
            pool_size=DB_POOL_SIZE,
            max_overflow=DB_MAX_OVERFLOW,
            pool_timeout=DB_POOL_TIMEOUT,
            pool_recycle=DB_POOL_RECYCLE,
            pool_pre_ping=True,  # 连接池预检查
            echo=False  # 生产环境关闭SQL日志
        )
        
        # 测试数据库连接
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            logger.info("数据库连接成功")
        
        # 创建会话工厂
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # 创建基类
        Base = declarative_base()
        
        # 设置Base的schema属性
        Base.metadata.schema = settings.DATABASE_SCHEMA
        
        logger.info("数据库初始化完成")
        return True
        
    except OperationalError as e:
        logger.critical(f"数据库连接失败 - 操作错误: {str(e)}")
        logger.critical(f"错误堆栈: {traceback.format_exc()}")
        raise Exception(f"数据库连接失败: {str(e)}")
    except SQLAlchemyError as e:
        logger.critical(f"数据库连接失败 - SQLAlchemy错误: {str(e)}")
        logger.critical(f"错误堆栈: {traceback.format_exc()}")
        raise Exception(f"数据库连接失败: {str(e)}")
    except Exception as e:
        logger.critical(f"数据库连接失败 - 未知错误: {str(e)}")
        logger.critical(f"错误堆栈: {traceback.format_exc()}")
        raise Exception(f"数据库连接失败: {str(e)}")


@contextmanager
def get_db_context():
    """
    获取数据库会话上下文管理器
    
    Returns:
        ContextManager[Session]: 数据库会话上下文管理器
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
        logger.debug("数据库事务提交成功")
    except Exception as e:
        db.rollback()
        # 只回滚事务，不捕获HTTPException等业务异常
        # 让业务异常正常传播给调用者
        if isinstance(e, (HTTPException, APIException)):
            # 不记录这些业务异常的堆栈，因为它们是预期内的
            logger.debug(f"业务异常 - 事务已回滚: {str(e)}")
            raise
        else:
            # 记录数据库相关异常的详细信息
            logger.error(f"数据库事务回滚 - 错误: {str(e)}")
            logger.error(f"错误堆栈: {traceback.format_exc()}")
            # 对于数据库异常，我们抛出带有详细信息的异常
            raise Exception(f"数据库操作错误: {str(e)}")
    finally:
        db.close()
        logger.debug("数据库会话已关闭")


def get_db():
    """
    获取数据库会话（用于FastAPI依赖注入）
    
    Yields:
        Session: 数据库会话
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
        logger.debug("数据库事务提交成功")
    except Exception as e:
        db.rollback()
        # 只回滚事务，不捕获HTTPException等业务异常
        # 让业务异常正常传播给FastAPI的异常处理器
        if isinstance(e, (HTTPException, APIException)):
            # 不记录这些业务异常的堆栈，因为它们是预期内的
            logger.debug(f"业务异常 - 事务已回滚: {str(e)}")
            raise
        else:
            # 记录数据库相关异常的详细信息
            logger.error(f"数据库事务回滚 - 错误: {str(e)}")
            logger.error(f"错误堆栈: {traceback.format_exc()}")
            # 对于数据库异常，我们抛出带有详细信息的异常
            raise Exception(f"数据库操作错误: {str(e)}")
    finally:
        db.close()
        logger.debug("数据库会话已关闭")


def create_tables():
    """
    创建数据库表
    
    Raises:
        Exception: 创建表失败时抛出
    """
    try:
        logger.info("开始创建数据库表...")
        # 导入所有模型，确保它们被注册到Base的metadata中
        from app.models import user
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
        return True
    except SQLAlchemyError as e:
        logger.error(f"创建数据库表失败 - SQLAlchemy错误: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise Exception(f"创建数据库表失败: {str(e)}")
    except Exception as e:
        logger.error(f"创建数据库表失败 - 未知错误: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise Exception(f"创建数据库表失败: {str(e)}")


def drop_tables():
    """
    删除数据库表
    
    Raises:
        Exception: 删除表失败时抛出
    """
    try:
        logger.warning("开始删除数据库表...")
        # 导入所有模型，确保它们被注册到Base的metadata中
        from app.models import user
        
        # 删除所有表
        Base.metadata.drop_all(bind=engine)
        logger.warning("数据库表删除成功")
        return True
    except SQLAlchemyError as e:
        logger.error(f"删除数据库表失败 - SQLAlchemy错误: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise Exception(f"删除数据库表失败: {str(e)}")
    except Exception as e:
        logger.error(f"删除数据库表失败 - 未知错误: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise Exception(f"删除数据库表失败: {str(e)}")

# 初始化数据库
init_database()