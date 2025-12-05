from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.auth.dependencies import get_current_user, optional_get_current_active_user
from app.models.user import User
from app.recipes.schemas import (
    RecipeBase, RecipeCreate, RecipeUpdate, RecipeResponse, RecipeListItem,
    RecipeSearchParams, RatingCreate, RatingResponse,
    NutritionInfoResponse, RecipeListResponse
)
from app.recipes.services import RecipeService

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("/", response_model=RecipeResponse)
async def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新食谱
    """
    # 转换Pydantic模型为字典
    recipe_data = recipe.model_dump()
    new_recipe = RecipeService.create_recipe(db, current_user.user_id, recipe_data)
    
    # 加载关联数据以构建完整响应
    full_recipe = RecipeService.get_recipe_by_id(db, new_recipe.recipe_id)
    
    # 处理食材信息，确保转换为List[SimpleIngredient]类型
    ingredients = []
    if full_recipe.ingredients:
        import json
        try:
            # 只有当ingredients是字符串类型时才进行JSON解析
            if isinstance(full_recipe.ingredients, str):
                parsed_ingredients = json.loads(full_recipe.ingredients)
            else:
                # 如果已经是列表类型，直接使用
                parsed_ingredients = full_recipe.ingredients
            
            # 确保ingredients是List[SimpleIngredient]类型
            for ing in parsed_ingredients:
                if isinstance(ing, dict) and 'name' in ing and 'quantity' in ing:
                    ingredients.append({
                        'name': ing['name'],
                        'quantity': ing['quantity'],
                        'unit': ing.get('unit')
                    })
        except (json.JSONDecodeError, TypeError):
            ingredients = []
    
    # 构建响应数据
    # 处理instructions，将字符串转换为数组
    instructions = full_recipe.instructions or ""
    if isinstance(instructions, str):
        instructions = [step.strip() for step in instructions.split('\n') if step.strip()]
    
    return RecipeResponse(
        recipe_id=str(full_recipe.recipe_id),
        title=full_recipe.title,
        description=full_recipe.description,
        instructions=instructions,
        cooking_time=full_recipe.cooking_time,
        servings=full_recipe.servings,
        difficulty=full_recipe.difficulty,
        ingredients=ingredients,
        tags=full_recipe.tags,
        image_url=full_recipe.image_url,
        nutrition_info=NutritionInfoResponse(
            nutrition_id=full_recipe.nutrition_info.nutrition_id,
            recipe_id=str(full_recipe.nutrition_info.recipe_id),
            calories=full_recipe.nutrition_info.calories,
            protein=full_recipe.nutrition_info.protein,
            carbohydrates=full_recipe.nutrition_info.carbs,
            fat=full_recipe.nutrition_info.fat,
            fiber=full_recipe.nutrition_info.fiber
        ) if full_recipe.nutrition_info else None,
        author_id=str(full_recipe.author_id),
        author_name=full_recipe.author.username,
        created_at=full_recipe.created_at,
        updated_at=full_recipe.updated_at
    )


@router.get("/user", response_model=List[RecipeListItem])
async def get_user_recipes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的食谱列表
    """
    recipes = RecipeService.get_recipes(
        db=db,
        author_id=current_user.user_id
    )
    
    # 构建响应
    return [
        RecipeListItem(
            recipe_id=str(recipe.recipe_id),
            title=recipe.title,
            description=recipe.description,
            cooking_time=recipe.cooking_time,
            difficulty=recipe.difficulty,
            tags=recipe.tags,
            image_url=recipe.image_url,
            author_id=str(recipe.author_id),
            author_name=recipe.author.username,
            created_at=recipe.created_at
        )
        for recipe in recipes
    ]


@router.get("/", response_model=RecipeListResponse)
async def get_recipes(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    page: Optional[int] = Query(None, ge=1),  # 新增：支持page参数
    tags: Optional[List[str]] = Query(None),  # 新增：支持tags参数
    author_id: Optional[str] = None,
    query: Optional[str] = None,
    difficulty: Optional[str] = None,
    max_cooking_time: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(optional_get_current_active_user)
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
    if tags:  # 新增：支持tags参数
        search_params["tags"] = tags
    
    # 如果提供了page参数，计算skip值
    if page is not None:
        skip = (page - 1) * limit
    
    # 获取当前用户ID（如果已登录）
    user_id = current_user.user_id if current_user else None
    
    # 获取食谱列表和总数
    recipes = RecipeService.get_recipes(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id,
        user_id=user_id,  # 传递当前用户ID用于过滤
        search_params=search_params if search_params else None
    )
    
    total = RecipeService.get_recipes_count(
        db=db,
        author_id=author_id,
        user_id=user_id,  # 传递当前用户ID用于过滤，确保总数也排除已收藏的食谱
        search_params=search_params if search_params else None
    )
    
    # 构建食谱列表项
    recipe_list_items = [
        RecipeListItem(
            recipe_id=str(recipe.recipe_id),
            title=recipe.title,
            description=recipe.description,
            cooking_time=recipe.cooking_time,
            difficulty=recipe.difficulty,
            author_name=recipe.author.username,
            image_url=recipe.image_url,
            created_at=recipe.created_at
        )
        for recipe in recipes
    ]
    
    # 构建响应
    return RecipeListResponse(
        recipes=recipe_list_items,
        page=page,
        limit=limit,
        total=total
    )


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
    # 将instructions字符串按换行符分割为数组，以匹配前端期望的格式
    instructions = recipe.instructions or ""
    # 如果是字符串，按换行符分割成数组；如果已经是数组，直接使用
    if isinstance(instructions, str):
        instructions = [step.strip() for step in instructions.split('\n') if step.strip()]
    
    # 处理食材信息，确保转换为List[SimpleIngredient]类型
    ingredients = []
    if recipe.ingredients:
        import json
        try:
            # 只有当ingredients是字符串类型时才进行JSON解析
            if isinstance(recipe.ingredients, str):
                parsed_ingredients = json.loads(recipe.ingredients)
            else:
                # 如果已经是列表类型，直接使用
                parsed_ingredients = recipe.ingredients
            
            # 确保ingredients是List[SimpleIngredient]类型
            for ing in parsed_ingredients:
                if isinstance(ing, dict) and 'name' in ing and 'quantity' in ing:
                    ingredients.append({
                        'name': ing['name'],
                        'quantity': ing['quantity'],
                        'unit': ing.get('unit')
                    })
        except (json.JSONDecodeError, TypeError):
            ingredients = []
    
    return RecipeResponse(
        recipe_id=str(recipe.recipe_id),
        title=recipe.title,
        description=recipe.description,
        instructions=instructions,
        cooking_time=recipe.cooking_time,
        servings=recipe.servings,
        difficulty=recipe.difficulty,
        ingredients=ingredients,
        tags=recipe.tags,
        image_url=recipe.image_url,
        nutrition_info=NutritionInfoResponse(
            nutrition_id=recipe.nutrition_info.nutrition_id,
            recipe_id=str(recipe.nutrition_info.recipe_id),
            calories=recipe.nutrition_info.calories,
            protein=recipe.nutrition_info.protein,
            carbs=recipe.nutrition_info.carbs,
            fat=recipe.nutrition_info.fat,
            fiber=recipe.nutrition_info.fiber
        ) if recipe.nutrition_info else None,
        author_id=str(recipe.author_id),
        author_name=recipe.author.username,
        created_at=recipe.created_at,
        updated_at=recipe.updated_at
    )


@router.put("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(
    recipe_id: str,
    recipe_update: RecipeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
        raise HTTPException(status_code=403, detail="You can only update your own recipes")
    
    # 更新食谱
    recipe_data = recipe_update.model_dump(exclude_unset=True)
    updated_recipe = RecipeService.update_recipe(db, recipe_id, recipe_data)
    
    if not updated_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # 重新获取完整数据
    full_recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    
    # 处理食材信息，确保转换为List[SimpleIngredient]类型
    ingredients = []
    if full_recipe.ingredients:
        import json
        try:
            # 只有当ingredients是字符串类型时才进行JSON解析
            if isinstance(full_recipe.ingredients, str):
                parsed_ingredients = json.loads(full_recipe.ingredients)
            else:
                # 如果已经是列表类型，直接使用
                parsed_ingredients = full_recipe.ingredients
            
            # 确保ingredients是List[SimpleIngredient]类型
            for ing in parsed_ingredients:
                if isinstance(ing, dict) and 'name' in ing and 'quantity' in ing:
                    ingredients.append({
                        'name': ing['name'],
                        'quantity': ing['quantity'],
                        'unit': ing.get('unit')
                    })
        except (json.JSONDecodeError, TypeError):
            ingredients = []
    
    # 构建响应
    # 处理instructions，将字符串转换为数组
    instructions = full_recipe.instructions or ""
    if isinstance(instructions, str):
        instructions = [step.strip() for step in instructions.split('\n') if step.strip()]
    
    return RecipeResponse(
        recipe_id=str(full_recipe.recipe_id),
        title=full_recipe.title,
        description=full_recipe.description,
        instructions=instructions,
        cooking_time=full_recipe.cooking_time,
        servings=full_recipe.servings,
        difficulty=full_recipe.difficulty,
        ingredients=ingredients,
        tags=full_recipe.tags,
        image_url=full_recipe.image_url,
        nutrition_info=NutritionInfoResponse(
            nutrition_id=full_recipe.nutrition_info.nutrition_id,
            recipe_id=str(full_recipe.nutrition_info.recipe_id),
            calories=full_recipe.nutrition_info.calories,
            protein=full_recipe.nutrition_info.protein,
            carbohydrates=full_recipe.nutrition_info.carbs,
            fat=full_recipe.nutrition_info.fat,
            fiber=full_recipe.nutrition_info.fiber
        ) if full_recipe.nutrition_info else None,
        author_id=str(full_recipe.author_id),
        author_name=full_recipe.author.username,
        created_at=full_recipe.created_at,
        updated_at=full_recipe.updated_at
    )




@router.delete("/{recipe_id}", status_code=204)
async def delete_recipe(
    recipe_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
        raise HTTPException(status_code=403, detail="You can only delete your own recipes")
    
    # 删除食谱
    success = RecipeService.delete_recipe(db, recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return None


@router.post("/{recipe_id}/rating", response_model=RatingResponse)
async def rate_recipe(
    recipe_id: str,
    rating_data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
        rating_id=rating.rating_id,
        user_id=str(current_user.user_id),
        recipe_id=recipe_id,
        score=rating.score,
        comment=rating.comment,
        created_at=rating.created_at,
        user_name=current_user.username
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
            rating_id=rating.rating_id,
            user_id=str(rating.user_id),
            recipe_id=rating.recipe_id,
            score=rating.score,
            comment=rating.comment,
            created_at=rating.created_at,
            user_name=rating.user.username
        )
        for rating in ratings
    ]


@router.post("/{recipe_id}/favorite", response_model=dict)
async def add_favorite(
    recipe_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    添加收藏
    """
    # 检查食谱是否存在
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # 添加收藏
    favorite = RecipeService.add_favorite(db, current_user.user_id, recipe_id)
    
    if not favorite:
        raise HTTPException(status_code=500, detail="Failed to add favorite")
    
    # 构建响应
    return {
        "message": "Recipe added to favorites",
        "is_favorite": True,
        "favorite_id": str(favorite.favorite_id)
    }


@router.delete("/{recipe_id}/favorite", response_model=dict)
async def remove_favorite(
    recipe_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    取消收藏
    """
    # 检查食谱是否存在
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # 取消收藏
    success = RecipeService.remove_favorite(db, current_user.user_id, recipe_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to remove favorite")
    
    # 构建响应
    return {
        "message": "Recipe removed from favorites",
        "is_favorite": False
    }


@router.get("/{recipe_id}/favorite", response_model=dict)
async def check_favorite(
    recipe_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    检查是否收藏
    """
    # 检查食谱是否存在
    recipe = RecipeService.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # 检查收藏状态
    is_favorite = RecipeService.is_favorite(db, current_user.user_id, recipe_id)
    
    # 构建响应
    return {
        "is_favorite": is_favorite
    }


