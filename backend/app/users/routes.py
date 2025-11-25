from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.auth.dependencies import get_current_user, get_current_superuser
from app.models.user import User
from app.auth.schemas import UserResponse, UserUpdate
from app.users.services import UserService

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户信息
    """
    current_user.user_id = str(current_user.user_id)
    return current_user

# 获取用户列表（管理员专用）
@router.get("", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    is_active: Optional[bool] = Query(None, description="筛选活跃状态"),
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    获取用户列表（仅管理员可访问）
    """
    users = UserService.get_users(db, skip=skip, limit=limit, is_active=is_active)
    return users

# 获取特定用户信息
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取特定用户信息
    - 普通用户只能查看自己的信息
    - 管理员可以查看所有用户的信息
    """
    # 检查权限
    if user_id != current_user.user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return user

# 更新用户信息（管理员专用）
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    更新用户信息（仅管理员可访问）
    """
    # 不允许管理员修改自己的角色
    if user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能修改自己的信息"
        )
    
    try:
        updated_user = UserService.update_user(db, user_id, **user_data.model_dump(exclude_unset=True))
        return updated_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# 停用用户（管理员专用）
@router.put("/{user_id}/deactivate")
async def deactivate_user(
    user_id: str,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    停用用户（仅管理员可访问）
    """
    # 不允许管理员停用自己
    if user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能停用自己的账号"
        )
    
    try:
        UserService.deactivate_user(db, user_id)
        return {"message": "用户已停用", "success": True}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# 激活用户（管理员专用）
@router.put("/{user_id}/activate")
async def activate_user(
    user_id: str,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    激活用户（仅管理员可访问）
    """
    try:
        UserService.activate_user(db, user_id)
        return {"message": "用户已激活", "success": True}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# 搜索用户
@router.get("/search/query", response_model=List[UserResponse])
async def search_users(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    搜索用户（根据用户名或显示名称）
    """
    users = UserService.search_users(db, query_text=q, skip=skip, limit=limit)
    return users

# 获取用户统计信息
@router.get("/stats/summary", response_model=dict)
async def get_user_stats(
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    获取用户统计信息（仅管理员可访问）
    """
    total_users = UserService.count_users(db)
    active_users = UserService.count_users(db, is_active=True)
    inactive_users = UserService.count_users(db, is_active=False)
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users
    }