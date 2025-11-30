from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Union, List
import logging
import secrets

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.auth.schemas import TokenData

# 配置日志记录器
logger = logging.getLogger(__name__)

# OAuth2密码Bearer流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 可选的令牌黑名单（生产环境中应使用Redis或数据库存储）
# 注意：这只是一个示例，生产环境应使用持久化存储
token_blacklist: List[str] = []


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间
        
    Returns:
        str: 生成的JWT令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 添加额外的安全声明
    to_encode.update({
        "exp": expire, 
        "iat": datetime.utcnow(), 
        "type": "access",
        "jti": secrets.token_urlsafe(16),  # JWT ID，用于撤销
        "version": "1.0"  # 令牌版本，便于将来升级
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    创建刷新令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间
        
    Returns:
        str: 生成的JWT令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    # 添加额外的安全声明
    to_encode.update({
        "exp": expire, 
        "iat": datetime.utcnow(), 
        "type": "refresh",
        "jti": secrets.token_urlsafe(16),  # JWT ID，用于撤销
        "version": "1.0"  # 令牌版本，便于将来升级
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def is_token_blacklisted(token: str) -> bool:
    """
    检查令牌是否在黑名单中
    
    Args:
        token: JWT令牌
        
    Returns:
        bool: 如果令牌在黑名单中返回True，否则返回False
    """
    # 提取令牌的JWT ID
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_signature": False})
        jti = payload.get("jti")
        if jti:
            return jti in token_blacklist
    except JWTError:
        pass
    return False


def blacklist_token(token: str) -> None:
    """
    将令牌添加到黑名单
    
    Args:
        token: JWT令牌
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_signature": False})
        jti = payload.get("jti")
        if jti and jti not in token_blacklist:
            token_blacklist.append(jti)
            logger.info(f"Token blacklisted: {jti}")
    except JWTError as e:
        logger.error(f"Error blacklisting token: {e}")


def verify_token(token: str, credentials_exception: HTTPException) -> TokenData:
    """
    验证令牌
    
    Args:
        token: JWT令牌
        credentials_exception: 认证异常
        
    Returns:
        TokenData: 令牌数据
    """
    # 检查令牌是否在黑名单中
    if is_token_blacklisted(token):
        logger.warning("Attempt to use blacklisted token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌已被撤销",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # 验证令牌签名和过期时间
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # 验证必要的声明
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.warning("Token missing 'sub' claim")
            raise credentials_exception
            
        token_type: str = payload.get("type")
        if token_type is None:
            logger.warning("Token missing 'type' claim")
            raise credentials_exception
        
        # 记录令牌验证成功
        logger.info(f"Token verified successfully for user_id: {user_id}, type: {token_type}")
        
        token_data = TokenData(user_id=user_id, token_type=token_type)
        return token_data
        
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTClaimsError as e:
        logger.warning(f"Token claims error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌声明无效",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        logger.warning(f"Token validation error: {e}")
        raise credentials_exception


def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    获取当前用户
    
    Args:
        request: HTTP请求对象，用于记录请求信息
        token: JWT令牌
        db: 数据库会话
        
    Returns:
        User: 当前用户
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 记录认证请求信息（不记录敏感数据）
    client_ip = request.client.host
    user_agent = request.headers.get("User-Agent", "Unknown")
    logger.info(f"Authentication attempt from IP: {client_ip}, User-Agent: {user_agent}")
    
    # 验证令牌
    token_data = verify_token(token, credentials_exception)
    
    # 验证令牌类型
    if token_data.token_type != "access":
        logger.warning(f"Invalid token type used: {token_data.token_type}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌类型",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 从数据库获取用户（使用带日志记录的方法，确保数据直接来自数据库）
    user = User.get_by_id(db, token_data.user_id)
    
    if user is None:
        logger.warning(f"User not found in database: {token_data.user_id}")
        raise credentials_exception
    
    # 检查用户是否被禁用
    if user.is_active != 'Y':
        logger.warning(f"Attempt to use disabled account: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账户已被禁用",
        )
    
    # 记录认证成功
    logger.info(f"Successful authentication for user: {user.username} (ID: {user.user_id})")
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    获取当前活跃用户
    
    Args:
        current_user: 当前用户
        
    Returns:
        User: 当前活跃用户
    """
    if current_user.is_active != 'Y':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账户已被禁用",
        )
    return current_user


def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    """
    获取当前超级用户
    
    Args:
        current_user: 当前用户
        
    Returns:
        User: 当前超级用户
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有足够的权限",
        )
    return current_user


def refresh_access_token(refresh_token: str, request: Request, db: Session) -> Dict[str, str]:
    """
    刷新访问令牌
    
    Args:
        refresh_token: 刷新令牌
        request: HTTP请求对象
        db: 数据库会话
        
    Returns:
        Dict[str, str]: 新的访问令牌和刷新令牌
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 记录刷新令牌请求
    client_ip = request.client.host
    logger.info(f"Token refresh attempt from IP: {client_ip}")
    
    try:
        # 验证刷新令牌
        if is_token_blacklisted(refresh_token):
            logger.warning("Attempt to use blacklisted refresh token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="刷新令牌已被撤销",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "refresh":
            logger.warning("Invalid refresh token format")
            raise credentials_exception
        
        # 从数据库获取用户（使用带日志记录的方法，确保数据直接来自数据库）
        user = User.get_by_id(db, user_id)
        if user is None:
            logger.warning(f"User not found during token refresh: {user_id}")
            raise credentials_exception
        
        # 检查用户是否被禁用
        if user.is_active != 'Y':
            logger.warning(f"Attempt to refresh token for disabled account: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户账户已被禁用",
            )
        
        # 将旧的刷新令牌添加到黑名单
        blacklist_token(refresh_token)
        
        # 创建新的访问令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.user_id)},
            expires_delta=access_token_expires,
        )
        
        # 创建新的刷新令牌
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        new_refresh_token = create_refresh_token(
            data={"sub": str(user.user_id)},
            expires_delta=refresh_token_expires,
        )
        
        logger.info(f"Token refresh successful for user: {user.username}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": new_refresh_token,
        }
        
    except jwt.ExpiredSignatureError:
        logger.warning("Refresh token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="刷新令牌已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        logger.error(f"JWT error during token refresh: {e}")
        raise credentials_exception