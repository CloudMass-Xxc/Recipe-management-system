from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.user import User
from app.users.services import UserService
from app.recipes.services import RecipeService
from app.recipes.schemas import FavoriteResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["用户管理"])
user_service = UserService()
recipe_service = RecipeService()

# 获取用户列表（暂时不实现身份验证）
@router.get("", response_model=List[dict])
async def get_users(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    db: Session = Depends(get_db)
):
    """
    获取用户列表（临时实现，无身份验证）
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return [{
        "user_id": str(user.user_id),
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "is_active": user.is_active == 'Y'
    } for user in users]

@router.get("/favorites", summary="获取当前用户的收藏列表", response_model=dict)
async def get_user_favorites(
    page: int = Query(1, ge=1, description="当前页码"),
    limit: int = Query(100, ge=1, le=1000, description="每页记录数"),
    skip: int = Query(None, ge=0, description="跳过的记录数"),
    search: str = Query(None, description="搜索关键词"),
    sort_by: str = Query("created_at", description="排序字段"),
    sort_order: str = Query("desc", description="排序方向"),
    difficulty: str = Query(None, description="难度筛选"),
    tags: List[str] = Query(None, description="标签筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前登录用户的所有收藏食谱"""
    try:
        # 兼容page和skip参数
        if skip is None:
            skip = (page - 1) * limit
        
        # 获取当前用户的收藏列表
        favorites = recipe_service.get_user_favorites(db, current_user.user_id, skip=skip, limit=limit)
        
        # 应用过滤和排序
        filtered_favorites = favorites
        
        # 搜索过滤
        if search:
            search_lower = search.lower()
            filtered_favorites = [
                fav for fav in filtered_favorites 
                if hasattr(fav, 'recipe') and fav.recipe and (
                    search_lower in fav.recipe.title.lower() or 
                    search_lower in fav.recipe.description.lower()
                )
            ]
        
        # 难度过滤
        if difficulty:
            filtered_favorites = [
                fav for fav in filtered_favorites 
                if hasattr(fav, 'recipe') and fav.recipe and 
                fav.recipe.difficulty == difficulty
            ]
        
        # 标签过滤
        if tags and len(tags) > 0:
            filtered_favorites = [
                fav for fav in filtered_favorites 
                if hasattr(fav, 'recipe') and fav.recipe and 
                all(tag in getattr(fav.recipe, 'tags', []) for tag in tags)
            ]
        
        # 排序
        def get_sort_key(fav):
            if not hasattr(fav, 'recipe') or not fav.recipe:
                return 0
            
            recipe = fav.recipe
            if sort_by == 'cooking_time':
                return recipe.cooking_time
            elif sort_by == 'difficulty':
                # 将难度转换为可排序的数值
                difficulty_order = {'简单': 1, '中等': 2, '困难': 3, 'easy': 1, 'medium': 2, 'hard': 3}
                return difficulty_order.get(recipe.difficulty, 0)
            elif sort_by == 'created_at':
                return recipe.created_at
            return 0
        
        filtered_favorites.sort(
            key=get_sort_key,
            reverse=sort_order == 'desc'
        )
        
        # 应用分页
        paginated_favorites = filtered_favorites[skip:skip+limit]
        total_favorites = len(filtered_favorites)
        
        # 转换数据结构，确保返回的数据与前端期望匹配
        # 特别是将Recipe对象转换为RecipeListItem格式
        formatted_recipes = []
        for fav in paginated_favorites:
            # 确保recipe对象存在
            if hasattr(fav, 'recipe') and fav.recipe:
                recipe = fav.recipe
                # 转换为前端期望的RecipeListItem格式
                formatted_recipe = {
                    "recipe_id": str(recipe.recipe_id),
                    "title": recipe.title,
                    "description": recipe.description,
                    "cooking_time": recipe.cooking_time,
                    "difficulty": recipe.difficulty,
                    "author_name": recipe.author.username if hasattr(recipe, 'author') and recipe.author else "",
                    "image_url": recipe.image_url,
                    "created_at": recipe.created_at,
                    "tags": getattr(recipe, 'tags', [])
                }
                formatted_recipes.append(formatted_recipe)
        
        # 返回与前端期望匹配的数据结构
        return {
            "recipes": formatted_recipes,
            "page": skip // limit + 1,
            "limit": limit,
            "total": total_favorites
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取收藏列表失败: {str(e)}"
        )



# 获取当前用户个人资料
@router.get("/me", summary="获取当前用户个人资料", response_model=dict)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前登录用户的个人资料
    """
    try:
        return {
            "user_id": str(current_user.user_id),
            "username": current_user.username,
            "display_name": current_user.display_name,
            "email": current_user.email,
            "phone": current_user.phone,
            "bio": current_user.bio,
            "avatar_url": current_user.avatar_url,
            "diet_preferences": current_user.diet_preferences,
            "created_at": current_user.created_at,
            "updated_at": current_user.updated_at
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取个人资料失败: {str(e)}"
        )

# 更新当前用户个人资料
@router.put("/me", summary="更新当前用户个人资料", response_model=dict)
async def update_current_user_profile(
    profile_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新当前登录用户的个人资料
    """
    try:
        # 验证并更新用户资料
        update_fields = {}
        
        # 允许更新的字段
        allowed_fields = ["display_name", "email", "phone", "bio", "avatar_url", "diet_preferences"]
        
        for field in allowed_fields:
            if field in profile_data:
                update_fields[field] = profile_data[field]
        
        # 更新用户信息
        updated_user = UserService.update_user(db, current_user.user_id, **update_fields)
        
        return {
            "user_id": str(updated_user.user_id),
            "username": updated_user.username,
            "display_name": updated_user.display_name,
            "email": updated_user.email,
            "phone": updated_user.phone,
            "bio": updated_user.bio,
            "avatar_url": updated_user.avatar_url,
            "diet_preferences": updated_user.diet_preferences,
            "created_at": updated_user.created_at,
            "updated_at": updated_user.updated_at
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新个人资料失败: {str(e)}"
        )

# 获取特定用户信息（暂时不实现身份验证）
@router.get("/{user_id}", response_model=dict)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
    
    from uuid import UUID
    try:
        user_uuid = UUID(user_id)
        user = db.query(User).filter(User.user_id == user_uuid).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        return {
            "user_id": str(user.user_id),
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "is_active": user.is_active == 'Y'
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的用户ID格式"
        )

# 更新用户信息（暂时不实现）
@router.put("/{user_id}")
async def update_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能暂未实现"
    )
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

# 停用用户（暂时不实现）
@router.put("/{user_id}/deactivate")
async def deactivate_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能暂未实现"
    )
    """
    停用用户（仅管理员可访问）
    """
    # 不允许管理员停用自己
    if user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能停用自己的账号"
        )
    


# 激活用户（暂时不实现）
@router.put("/{user_id}/activate")
async def activate_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能暂未实现"
    )
    """
    激活用户（仅管理员可访问）
    """


# 搜索用户（暂时不实现）
@router.get("/search/query")
async def search_users(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    db: Session = Depends(get_db)
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能暂未实现"
    )
    """
    搜索用户（根据用户名或显示名称）
    """

# 获取用户统计信息（暂时不实现）
@router.get("/stats/summary")
async def get_user_stats(
    db: Session = Depends(get_db)
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="功能暂未实现"
    )
    """
    获取用户统计信息（仅管理员可访问）
    """
