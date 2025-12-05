from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import logging
import traceback

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# OAuth2 密码承载令牌策略
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    
    Args:
        data: 要编码到令牌中的数据
        expires_delta: 令牌过期时间
    
    Returns:
        str: 生成的JWT令牌
    """
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)  # 使用配置的过期时间
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.info(f"创建访问令牌成功 - 用户名: {data.get('sub')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"创建访问令牌失败: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建访问令牌失败"
        )


def verify_token(token: str) -> Dict[str, Any]:
    """
    验证令牌
    
    Args:
        token: JWT令牌字符串
        
    Returns:
        Dict[str, Any]: 解码后的令牌数据
        
    Raises:
        JWTError: 令牌验证失败
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            logger.warning("令牌验证失败 - 用户名不存在于令牌中")
            raise JWTError("用户名不存在于令牌中")
        logger.info(f"令牌验证成功 - 用户名: {username}")
        return payload
    except JWTError as e:
        logger.warning(f"令牌验证失败 - JWT错误: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"令牌验证失败 - 未知错误: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise JWTError(f"验证令牌时发生未知错误: {str(e)}")


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    获取当前用户
    
    Args:
        request: HTTP请求对象
        token: JWT令牌
        db: 数据库会话
        
    Returns:
        User: 当前登录用户对象
        
    Raises:
        HTTPException: 认证失败时抛出
    """
    client_ip = request.client.host
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 验证令牌
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            logger.warning(f"获取用户失败 - 令牌中用户名不存在, IP: {client_ip}")
            raise credentials_exception
    except JWTError:
        logger.warning(f"获取用户失败 - 令牌验证错误, IP: {client_ip}")
        raise credentials_exception
    
    # 查询用户
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        logger.warning(f"获取用户失败 - 用户不存在: {username}, IP: {client_ip}")
        raise credentials_exception
    
    # 检查用户是否被锁定
    if user.locked_until:
        logger.warning(f"获取用户失败 - 用户已被锁定: {username}, IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被锁定，请稍后再试"
        )
    
    # 检查用户是否激活
    if user.is_active != 'Y':
        logger.warning(f"获取用户失败 - 用户已被停用: {username}, IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被停用"
        )
    
    logger.info(f"获取用户成功 - 用户名: {username}, IP: {client_ip}")
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    获取当前活跃用户
    
    Args:
        current_user: 当前用户对象
        
    Returns:
        User: 当前活跃用户对象
    """
    try:
        logger.info(f"获取活动用户成功 - 用户名: {current_user.username}")
        return current_user
    except Exception as e:
        logger.error(f"获取活动用户失败: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户状态时发生错误"
        )


async def optional_get_current_active_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """
    获取当前活跃用户（可选）
    
    与get_current_active_user不同，当没有提供有效的令牌时，此函数返回None而不是抛出异常。
    适用于需要根据用户登录状态进行不同处理的API端点。
    
    Args:
        request: HTTP请求对象
        db: 数据库会话
        
    Returns:
        Optional[User]: 当前登录用户对象，如果未登录则返回None
    """
    try:
        # 尝试从请求头中获取令牌
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            logger.info("未提供有效的Authorization头")
            return None
        
        token = authorization.split(" ")[1]
        # 验证令牌
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            logger.warning("令牌中用户名不存在")
            return None
        
        # 查询用户
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            logger.warning(f"用户不存在: {username}")
            return None
        
        # 检查用户是否被锁定
        if user.locked_until:
            logger.warning(f"用户已被锁定: {username}")
            return None
        
        # 检查用户是否激活
        if user.is_active != 'Y':
            logger.warning(f"用户已被停用: {username}")
            return None
        
        logger.info(f"获取用户成功 - 用户名: {username}")
        return user
    except JWTError:
        logger.info("令牌验证错误，返回None")
        return None
    except Exception as e:
        logger.error(f"获取可选用户失败: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        return None
