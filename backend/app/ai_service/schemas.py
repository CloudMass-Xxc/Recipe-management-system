from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum


class DietaryPreference(str, Enum):
    """
    饮食偏好枚举
    """
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    MEAT = "meat"
    FISH = "fish"
    KETO = "keto"
    LOW_CARB = "low_carb"
    HIGH_PROTEIN = "high_protein"
    NONE = "none"


class Difficulty(str, Enum):
    """
    难度级别枚举
    """
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Ingredient(BaseModel):
    """
    食材模型
    """
    name: str = Field(..., description="食材名称")
    quantity: float = Field(..., description="数量")
    unit: str = Field(..., description="单位")
    note: Optional[str] = Field(None, description="备注")


class NutritionInfo(BaseModel):
    """
    营养信息模型
    """
    calories: int = Field(..., description="卡路里(千卡)")
    protein: float = Field(..., description="蛋白质(克)")
    carbs: float = Field(..., description="碳水化合物(克)")
    fat: float = Field(..., description="脂肪(克)")
    fiber: float = Field(..., description="膳食纤维(克)")
    
    @validator('calories', 'protein', 'carbs', 'fat', 'fiber')
    def non_negative(cls, v):
        if v < 0:
            raise ValueError('营养值不能为负数')
        return v


class RecipeGenerationRequest(BaseModel):
    """
    食谱生成请求模型
    """
    dietary_preferences: List[DietaryPreference] = Field(default=[], description="饮食偏好")
    food_likes: List[str] = Field(default=[], description="喜欢的食物")
    food_dislikes: List[str] = Field(default=[], description="不喜欢的食物")
    health_conditions: List[str] = Field(default=[], description="健康状况")
    nutrition_goals: List[str] = Field(default=[], description="营养目标")
    cooking_time_limit: Optional[int] = Field(None, description="烹饪时间限制(分钟)")
    difficulty: Optional[Difficulty] = Field(None, description="难度级别")
    
    @validator('cooking_time_limit')
    def validate_cooking_time(cls, v):
        if v is not None and v <= 0:
            raise ValueError('烹饪时间限制必须大于0')
        return v


class RecipeResponse(BaseModel):
    """
    食谱响应模型
    """
    title: str = Field(..., description="食谱标题")
    description: str = Field(..., description="食谱描述")
    prep_time: int = Field(..., description="准备时间(分钟)")
    cooking_time: int = Field(..., description="烹饪时间(分钟)")
    servings: int = Field(..., description="份量")
    difficulty: Difficulty = Field(..., description="难度级别")
    ingredients: List[Ingredient] = Field(..., description="食材列表")
    instructions: List[str] = Field(..., description="烹饪步骤")
    nutrition_info: NutritionInfo = Field(..., description="营养信息")
    tips: Optional[List[str]] = Field(None, description="烹饪小贴士")
    tags: Optional[List[str]] = Field(None, description="标签")
    
    @validator('prep_time', 'cooking_time', 'servings')
    def positive_values(cls, v):
        if v <= 0:
            raise ValueError('时间和份量必须为正数')
        return v


class RecipeEnhancementRequest(BaseModel):
    """
    食谱增强请求模型
    """
    recipe_data: Dict[str, Any] = Field(..., description="原始食谱数据")
    enhancement_request: str = Field(..., description="增强要求描述")
    
    @validator('enhancement_request')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('增强要求不能为空')
        return v


class SaveRecipeRequest(BaseModel):
    """
    保存食谱请求模型
    """
    recipe_data: RecipeResponse = Field(..., description="食谱数据")
    share_with_community: bool = Field(False, description="是否分享到社区")


class AIServiceStatus(BaseModel):
    """
    AI服务状态模型
    """
    status: str = Field(..., description="服务状态(available/unavailable)")
    provider: str = Field(..., description="服务提供商")
    version: str = Field(..., description="API版本")
    message: Optional[str] = Field(None, description="状态消息")