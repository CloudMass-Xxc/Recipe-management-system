from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.core.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.ai_service.schemas import (
    RecipeGenerationRequest,
    RecipeResponse,
    RecipeEnhancementRequest,
    SaveRecipeRequest,
    AIServiceStatus,
    Cuisine
)
from app.ai_service.ai_client import ai_client
from app.ai_service.exceptions import (
    AIServiceError,
    InvalidRecipeParametersError,
    RecipeGenerationError,
    RecipeEnhancementError
)
from app.recipes.services import RecipeService
from app.ai_service.config import get_ai_settings
from app.models.recipe import Recipe
import logging

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/status", response_model=AIServiceStatus)
async def get_ai_service_status():
    """
    获取AI服务状态
    """
    settings = get_ai_settings()
    
    # 检查通义千问API密钥
    is_available = bool(settings.QWEN_API_KEY)
    status = "available" if is_available else "unavailable"
    message = "AI service is ready to use" if is_available else "QWEN API key not configured"
    
    return AIServiceStatus(
        status=status,
        provider=settings.API_PROVIDER,
        version="1.0.0",
        message=message
    )


@router.post("/generate-recipe", response_model=RecipeResponse)
async def generate_recipe(
    request: RecipeGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    生成个性化食谱并自动保存到公共食谱列表
    """
    try:
        # 记录完整请求参数，包括具体的值
        logger.info(f"接收到食谱生成请求: {request.model_dump(exclude_none=True)}")
        logger.info(f"饮食偏好类型: {type(request.dietary_preferences)}")
        logger.info(f"饮食偏好值: {[p.value for p in request.dietary_preferences]}")
        logger.info(f"难度级别值: {request.difficulty.value if request.difficulty else None}")
        logger.info(f"菜系值: {request.cuisine.value}")
        logger.info(f"用户选择的食材: {request.ingredients}")
        
        # 调用AI客户端生成食谱
        logger.info("调用AI客户端生成食谱")
        
        # 直接传递请求对象的model_dump()给AI客户端，确保包含所有必要参数
        recipe_data = await ai_client.generate_recipe(request.model_dump())
        logger.info(f"AI客户端返回食谱数据，标题: {recipe_data.get('title', '未命名')}")
        
        # 自动将生成的食谱保存到公共食谱列表
        logger.info("自动保存生成的食谱到公共食谱列表")
        
        # 准备食谱数据用于保存
        save_data = {
            "title": recipe_data.get("title"),
            "description": recipe_data.get("description"),
            "instructions": "\n".join(recipe_data.get("instructions", [])),
            "ingredients": recipe_data.get("ingredients", []),
            "cooking_time": recipe_data.get("cooking_time", 0),
            "servings": recipe_data.get("servings", 1),
            "difficulty": recipe_data.get("difficulty", "easy"),
            "tags": recipe_data.get("tags", []),
            "image_url": recipe_data.get("image_url"),
            "nutrition_info": recipe_data.get("nutrition_info")
        }
        
        # 保存食谱到数据库（作为公共食谱）
        new_recipe = RecipeService.create_recipe(db, current_user.user_id, save_data)
        logger.info(f"食谱已成功保存到公共列表，ID: {new_recipe.recipe_id}")
        
        # 更新响应中的recipe_id为保存后的ID
        recipe_data["recipe_id"] = str(new_recipe.recipe_id)
        
        # 转换为响应模型
        response = RecipeResponse(**recipe_data)
        logger.info(f"食谱生成和保存成功，标题: {response.title}")
        return response
        
    except AIServiceError as e:
        logger.error(f"AI服务错误: {str(e)}", exc_info=True)
        raise e
    except Exception as e:
        logger.error(f"食谱生成失败: {str(e)}", exc_info=True)
        raise RecipeGenerationError(f"Failed to generate recipe: {str(e)}")


@router.post("/enhance-recipe", response_model=RecipeResponse)
async def enhance_recipe(
    request: RecipeEnhancementRequest,
    current_user: User = Depends(get_current_user)
):
    """
    增强或修改现有食谱
    """
    try:
        # 调用AI客户端增强食谱
        enhanced_recipe = await ai_client.enhance_recipe(
            request.recipe_data,
            request.enhancement_request
        )
        
        # 转换为响应模型
        return RecipeResponse(**enhanced_recipe)
        
    except AIServiceError as e:
        raise e
    except Exception as e:
        raise RecipeEnhancementError(f"Failed to enhance recipe: {str(e)}")


@router.post("/save-generated-recipe")
async def save_generated_recipe(
    request: SaveRecipeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    保存AI生成的食谱到用户账户，包括食谱配图
    """
    try:
        # 准备食谱数据
        recipe_data = request.recipe_data.model_dump()
        
        # 将烹饪步骤从列表转换为字符串
        if isinstance(recipe_data.get("instructions"), list):
            recipe_data["instructions"] = "\n".join(recipe_data["instructions"])
        
        # 将tips从列表转换为字符串
        if "tips" in recipe_data and isinstance(recipe_data["tips"], list):
            recipe_data["tips"] = "\n".join(recipe_data["tips"])
        
        # 移除不需要的字段
        recipe_data.pop("tips", None)
        recipe_data.pop("prep_time", None)
        
        # 检查是否有图片URL
        if "image_url" in recipe_data:
            logger.info(f"食谱包含图片URL: {recipe_data['image_url']}")
        else:
            logger.warning("食谱不包含图片URL")
        
        # 保存食谱
        new_recipe = RecipeService.create_recipe(db, current_user.user_id, recipe_data)
        
        # 获取完整的食谱数据（包括关联信息）
        full_recipe = RecipeService.get_recipe_by_id(db, new_recipe.recipe_id)
        
        # 将SQLAlchemy模型转换为字典，确保包含所有必要字段
        result = {
            "recipe_id": full_recipe.recipe_id,
            "title": full_recipe.title,
            "description": full_recipe.description,
            "difficulty": full_recipe.difficulty,
            "cooking_time": full_recipe.cooking_time,
            "servings": full_recipe.servings,
            "instructions": full_recipe.instructions,
            "ingredients": full_recipe.ingredients,
            "image": full_recipe.image_url,  # 返回image字段供前端使用
            "created_at": full_recipe.created_at.isoformat() if full_recipe.created_at else None,
            "updated_at": full_recipe.updated_at.isoformat() if full_recipe.updated_at else None,
            "author_id": full_recipe.author_id
        }
        
        # 添加营养信息
        if full_recipe.nutrition_info:
            result["nutrition_info"] = {
                "calories": full_recipe.nutrition_info.calories,
                "protein": full_recipe.nutrition_info.protein,
                "carbs": full_recipe.nutrition_info.carbs,
                "fat": full_recipe.nutrition_info.fat,
                "fiber": full_recipe.nutrition_info.fiber
            }
        
        # 添加标签
        if full_recipe.tags:
            result["tags"] = full_recipe.tags
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save recipe: {str(e)}"
        )


@router.post("/analyze-nutrition")
async def analyze_nutrition(
    ingredients: list[dict],
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    分析食材的营养成分
    """
    try:
        # 构建提示词
        ingredients_text = "\n".join([
            f"- {ing['quantity']} {ing['unit']} {ing['name']}"
            for ing in ingredients
        ])
        
        prompt = f"""
请分析以下食材的总营养成分：

{ingredients_text}

请以JSON格式输出，包含以下字段：
- calories: 总卡路里(千卡)
- protein: 总蛋白质(克)
- carbs: 总碳水化合物(克)
- fat: 总脂肪(克)
- fiber: 总膳食纤维(克)
- summary: 简短的营养评估
"""
        
        # 调用AI客户端进行分析
        import json
        from app.ai_service.config import get_ai_settings
        settings = get_ai_settings()
        
        request_body = ai_client._prepare_chat_completion_request(prompt)
        # 修复：移除URL参数，直接调用_make_async_request
        response = await ai_client._make_async_request(request_body)
        
        # 根据不同的API提供商获取响应内容
        if settings.API_PROVIDER == "alipan":
            content = response.get("output", {}).get("text", "")
        else:
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # 尝试提取和解析JSON
        try:
            # 尝试直接解析
            nutrition_data = json.loads(content)
        except json.JSONDecodeError:
            # 尝试提取JSON格式的部分
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                nutrition_data = json.loads(json_match.group())
            else:
                raise ValueError("无法从AI响应中提取有效的JSON数据")
        
        return nutrition_data
        
    except Exception as e:
        logger.error(f"营养分析失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"营养分析失败: {str(e)}"
        )