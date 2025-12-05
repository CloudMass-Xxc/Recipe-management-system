from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.auth.jwt import get_current_user, get_current_active_user, optional_get_current_active_user


async def get_current_superuser(current_user: User = Depends(get_current_active_user)) -> User:
    """
    获取当前超级用户（管理员）
    
    Args:
        current_user: 当前活跃用户对象
        
    Returns:
        User: 当前超级用户对象
        
    Raises:
        HTTPException: 不是超级用户时抛出
    """
    # 这里可以根据实际需求调整超级用户的判断逻辑
    # 例如，检查用户是否有特定角色或权限
    # 目前暂时不实现超级用户功能
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="超级用户功能暂未实现"
    )
