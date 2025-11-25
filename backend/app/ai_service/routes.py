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
    
    # 根据不同的API提供商检查相应的API密钥
    if settings.API_PROVIDER == "alipan":
        is_available = bool(settings.QWEN_API_KEY)
        status = "available" if is_available else "unavailable"
        message = "AI service is ready to use" if is_available else "QWEN API key not configured"
    else:
        is_available = bool(settings.OPENAI_API_KEY)
        status = "available" if is_available else "unavailable"
        message = "AI service is ready to use" if is_available else "OpenAI API key not configured"
    
    return AIServiceStatus(
        status=status,
        provider=settings.API_PROVIDER,
        version="1.0.0",
        message=message
    )


@router.post("/generate-recipe", response_model=RecipeResponse)
async def generate_recipe(
    request: RecipeGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    生成个性化食谱
    """
    try:
        # 记录完整请求参数，包括具体的值
        logger.info(f"接收到食谱生成请求: {request.model_dump(exclude_none=True)}")
        logger.info(f"饮食偏好类型: {type(request.dietary_preferences)}")
        logger.info(f"饮食偏好值: {[p.value for p in request.dietary_preferences]}")
        logger.info(f"难度级别值: {request.difficulty.value if request.difficulty else None}")
        logger.info(f"菜系值: {request.cuisine.value}")
        
        # 准备食谱生成参数
        dietary_preferences = ", ".join([p.value for p in request.dietary_preferences])
        logger.info(f"处理后饮食偏好: {dietary_preferences}")
        
        food_likes = ", ".join(request.food_likes)
        food_dislikes = ", ".join(request.food_dislikes)
        health_conditions = ", ".join(request.health_conditions)
        nutrition_goals = ", ".join(request.nutrition_goals)
        
        # 确保cooking_time_limit是整数类型
        cooking_time_limit_value = request.cooking_time_limit
        if cooking_time_limit_value is not None:
            cooking_time_limit_value = int(cooking_time_limit_value)
        cooking_time_limit = str(cooking_time_limit_value) if cooking_time_limit_value else "无限制"
        logger.info(f"处理后烹饪时间限制: {cooking_time_limit}")
        
        difficulty = request.difficulty.value if request.difficulty else "任意"
        logger.info(f"处理后难度级别: {difficulty}")
        
        cuisine = request.cuisine.value if request.cuisine != Cuisine.NONE else "不限"
        logger.info(f"处理后菜系: {cuisine}")
        
        recipe_params = {
            "dietary_preferences": dietary_preferences,
            "food_likes": food_likes,
            "food_dislikes": food_dislikes,
            "health_conditions": health_conditions,
            "nutrition_goals": nutrition_goals,
            "cooking_time_limit": cooking_time_limit,
            "difficulty": difficulty,
            "cuisine": cuisine
        }
        
        # 调用AI客户端生成食谱
        logger.info("调用AI客户端生成食谱")
        # 确保传递原始的cooking_time_limit_value（数值类型）给AI客户端
        ai_params = {
            "dietary_preferences": dietary_preferences,
            "food_likes": food_likes,
            "food_dislikes": food_dislikes,
            "health_conditions": health_conditions,
            "nutrition_goals": nutrition_goals,
            "cooking_time_limit": cooking_time_limit_value,  # 使用数值类型
            "difficulty": difficulty,
            "cuisine": cuisine
        }
        recipe_data = await ai_client.generate_recipe(ai_params)
        logger.info(f"AI客户端返回食谱数据，标题: {recipe_data.get('title', '未命名')}")
        
        # 转换为响应模型
        response = RecipeResponse(**recipe_data)
        logger.info(f"食谱生成成功，标题: {response.title}")
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
    保存AI生成的食谱到用户账户
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
        
        # 保存食谱
        new_recipe = RecipeService.create_recipe(db, current_user.user_id, recipe_data)
        
        return {
            "success": True,
            "recipe_id": new_recipe.recipe_id,
            "message": "Recipe saved successfully"
        }
        
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