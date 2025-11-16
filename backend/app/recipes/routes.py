from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.auth.dependencies import get_current_user, get_current_active_user
from app.auth.exceptions import PermissionDeniedException
from app.models.user import User
from app.recipes.schemas import (
    RecipeBase, RecipeCreate, RecipeUpdate, RecipeResponse, RecipeListItem,
    RecipeSearchParams, FavoriteResponse, RatingCreate, RatingResponse,
    NutritionInfoResponse
)
from app.recipes.services import RecipeService

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("/", response_model=RecipeResponse)
async def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建新食谱
    """
    # 转换Pydantic模型为字典
    recipe_data = recipe.model_dump()
    new_recipe = RecipeService.create_recipe(db, current_user.user_id, recipe_data)
    
    # 加载关联数据以构建完整响应
    full_recipe = RecipeService.get_recipe_by_id(db, new_recipe.recipe_id)
    
    # 构建响应数据
    return RecipeResponse(
        recipe_id=full_recipe.recipe_id,
        title=full_recipe.title,
        description=full_recipe.description,
        instructions=full_recipe.instructions,
        prep_time=full_recipe.prep_time,
        cooking_time=full_recipe.cooking_time,
        servings=full_recipe.servings,
        difficulty=full_recipe.difficulty,
        tags=full_recipe.tags,
        image_url=full_recipe.image_url,
        nutrition_info=NutritionInfoResponse(
            calories=full_recipe.nutrition_info.calories,
            protein=full_recipe.nutrition_info.protein,
            carbs=full_recipe.nutrition_info.carbs,
            fat=full_recipe.nutrition_info.fat,
            fiber=full_recipe.nutrition_info.fiber
        ) if full_recipe.nutrition_info else None,
        author_id=full_recipe.author_id,
        author_name=full_recipe.author.username,
        created_at=full_recipe.created_at,
        updated_at=full_recipe.updated_at
    )


@router.get("/", response_model=List[RecipeListItem])
async def get_recipes(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    author_id: Optional[str] = None,
    query: Optional[str] = None,
    difficulty: Optional[str] = None,
    max_cooking_time: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    获取食谱列表
    """
    # 构建搜索参数
    search_params = {}
    if query:
        search_params["query"] = query
    if difficulty:
        search_params["difficulty"] = difficulty
    if max_cooking_time is not None:
        search_params["max_cooking_time"] = max_cooking_time
    
    recipes = RecipeService.get_recipes(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id,
        search_params=search_params if search_params else None
    )
    
    # 构建响应
    return [
        RecipeListItem(
            recipe_id=recipe.recipe_id,
            title=recipe.title,
            description=recipe.description,
            prep_time=recipe.prep_time,
            cooking_time=recipe.cooking_time,
            difficulty=recipe.difficulty,
            tags=recipe.tags,
            image_url=recipe.image_url,
            author_id=recipe.author_id,
            author_name=recipe.author.username,
            created_at=recipe.created_at
        )
        for recipe in recipes
    ]


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(
    recipe_id: str,
    db: Session = Depends(get_db)
):
    """
    获取食谱详情
    """
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # 构建响应数据
    return RecipeResponse(
        recipe_id=recipe.recipe_id,
        title=recipe.title,
        description=recipe.description,
        instructions=recipe.instructions,
        prep_time=recipe.prep_time,
        cooking_time=recipe.cooking_time,
        servings=recipe.servings,
        difficulty=recipe.difficulty,
        tags=recipe.tags,
        image_url=recipe.image_url,
        nutrition_info=NutritionInfoResponse(
            calories=recipe.nutrition_info.calories,
            protein=recipe.nutrition_info.protein,
            carbs=recipe.nutrition_info.carbs,
            fat=recipe.nutrition_info.fat,
            fiber=recipe.nutrition_info.fiber
        ) if recipe.nutrition_info else None,
        author_id=recipe.author_id,
        author_name=recipe.author.username,
        created_at=recipe.created_at,
        updated_at=recipe.updated_at
    )


@router.put("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: str,
    recipe_update: RecipeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新食谱
    """
    # 检查食谱是否存在
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # 检查权限
    if recipe.author_id != current_user.user_id and not current_user.is_superuser:
        raise PermissionDeniedException("You can only update your own recipes")
    
    # 更新食谱
    recipe_data = recipe_update.model_dump(exclude_unset=True)
    updated_recipe = RecipeService.update_recipe(db, recipe_id, recipe_data)
    
    if not updated_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # 重新获取完整数据
    full_recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    
    # 构建响应
    return RecipeResponse(
        recipe_id=full_recipe.recipe_id,
        title=full_recipe.title,
        description=full_recipe.description,
        instructions=full_recipe.instructions,
        prep_time=full_recipe.prep_time,
        cooking_time=full_recipe.cooking_time,
        servings=full_recipe.servings,
        difficulty=full_recipe.difficulty,
        tags=full_recipe.tags,
        image_url=full_recipe.image_url,
        nutrition_info=NutritionInfoResponse(
            calories=full_recipe.nutrition_info.calories,
            protein=full_recipe.nutrition_info.protein,
            carbs=full_recipe.nutrition_info.carbs,
            fat=full_recipe.nutrition_info.fat,
            fiber=full_recipe.nutrition_info.fiber
        ) if full_recipe.nutrition_info else None,
        author_id=full_recipe.author_id,
        author_name=full_recipe.author.username,
        created_at=full_recipe.created_at,
        updated_at=full_recipe.updated_at
    )


@router.delete("/{recipe_id}", status_code=204)
async def delete_recipe(
    recipe_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除食谱
    """
    # 检查食谱是否存在
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # 检查权限
    if recipe.author_id != current_user.user_id and not current_user.is_superuser:
        raise PermissionDeniedException("You can only delete your own recipes")
    
    # 删除食谱
    success = RecipeService.delete_recipe(db, recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return None


@router.post("/{recipe_id}/favorite", response_model=FavoriteResponse)
async def favorite_recipe(
    recipe_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    收藏食谱
    """
    # 检查食谱是否存在
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # 收藏食谱
    favorite = RecipeService.favorite_recipe(db, current_user.user_id, recipe_id)
    if not favorite:
        raise HTTPException(status_code=400, detail="Already favorited")
    
    return FavoriteResponse(
        user_id=current_user.user_id,
        recipe_id=recipe_id,
        created_at=favorite.created_at
    )


@router.delete("/{recipe_id}/favorite", status_code=204)
async def unfavorite_recipe(
    recipe_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    取消收藏食谱
    """
    success = RecipeService.unfavorite_recipe(db, current_user.user_id, recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Not favorited")
    
    return None


@router.post("/{recipe_id}/rating", response_model=RatingResponse)
async def rate_recipe(
    recipe_id: str,
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    评分食谱
    """
    # 检查食谱是否存在
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # 评分食谱
    rating = RecipeService.rate_recipe(
        db, 
        current_user.user_id, 
        recipe_id, 
        rating_data.score,
        rating_data.comment
    )
    
    return RatingResponse(
        user_id=current_user.user_id,
        recipe_id=recipe_id,
        score=rating.score,
        comment=rating.comment,
        created_at=rating.created_at,
        username=current_user.username
    )


@router.get("/{recipe_id}/ratings", response_model=List[RatingResponse])
async def get_recipe_ratings(
    recipe_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    获取食谱评分列表
    """
    # 检查食谱是否存在
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # 获取评分列表
    ratings = RecipeService.get_recipe_ratings(db, recipe_id, skip, limit)
    
    # 构建响应
    return [
        RatingResponse(
            user_id=rating.user_id,
            recipe_id=rating.recipe_id,
            score=rating.score,
            comment=rating.comment,
            created_at=rating.created_at,
            username=rating.user.username
        )
        for rating in ratings
    ]


@router.get("/user/favorites", response_model=List[RecipeListItem])
async def get_user_favorites(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取用户收藏的食谱列表
    """
    favorites = RecipeService.get_user_favorites(db, current_user.user_id, skip, limit)
    
    # 构建响应
    return [
        RecipeListItem(
            recipe_id=favorite.recipe.recipe_id,
            title=favorite.recipe.title,
            description=favorite.recipe.description,
            prep_time=favorite.recipe.prep_time,
            cooking_time=favorite.recipe.cooking_time,
            difficulty=favorite.recipe.difficulty,
            tags=favorite.recipe.tags,
            image_url=favorite.recipe.image_url,
            author_id=favorite.recipe.author_id,
            author_name=favorite.recipe.author.username,
            created_at=favorite.recipe.created_at
        )
        for favorite in favorites
    ]