from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.auth.jwt import get_user_id_from_token
from app.auth.exceptions import CredentialsException
from app.models.user import User

# 创建OAuth2密码流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 获取当前用户
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    获取当前用户
    
    Args:
        token: JWT令牌
        db: 数据库会话
    
    Returns:
        当前用户对象
    
    Raises:
        CredentialsException: 如果凭证无效
    """
    user_id = get_user_id_from_token(token)
    if user_id is None:
        raise CredentialsException()
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise CredentialsException()
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )
    
    return user

# 获取当前活跃用户
async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    获取当前活跃用户
    
    Args:
        current_user: 当前用户
    
    Returns:
        当前活跃用户
    
    Raises:
        HTTPException: 如果用户不活跃
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )
    return current_user

# 获取当前超级用户
async def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    """
    获取当前超级用户
    
    Args:
        current_user: 当前用户
    
    Returns:
        当前超级用户
    
    Raises:
        HTTPException: 如果用户不是超级用户
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return current_user