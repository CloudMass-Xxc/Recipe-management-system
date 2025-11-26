from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal

# 营养信息基础模型
class NutritionInfoBase(BaseModel):
    calories: float = Field(..., gt=0, description="卡路里")
    protein: float = Field(..., ge=0, description="蛋白质(g)")
    carbohydrates: float = Field(..., ge=0, description="碳水化合物(g)")
    fat: float = Field(..., ge=0, description="脂肪(g)")
    fiber: Optional[float] = Field(None, ge=0, description="纤维(g)")
    sugar: Optional[float] = Field(None, ge=0, description="糖(g)")
    sodium: Optional[float] = Field(None, ge=0, description="钠(mg)")
    additional_nutrients: Optional[Dict[str, Any]] = Field(None, description="其他营养信息")

# 营养信息响应模型
class NutritionInfoResponse(NutritionInfoBase):
    nutrition_id: int = Field(..., description="营养信息ID")
    recipe_id: str = Field(..., description="食谱ID")
    
    class Config:
        from_attributes = True

# 食谱配料基础模型
class RecipeIngredientBase(BaseModel):
    ingredient_id: int = Field(..., description="食材ID")
    quantity: float = Field(..., gt=0, description="数量")
    unit: Optional[str] = Field(None, description="单位")
    note: Optional[str] = Field(None, description="备注")

# 食谱配料响应模型
class RecipeIngredientResponse(RecipeIngredientBase):
    recipe_ingredient_id: int = Field(..., description="配料ID")
    recipe_id: str = Field(..., description="食谱ID")
    ingredient_name: Optional[str] = Field(None, description="食材名称")
    
    class Config:
        from_attributes = True

# 简化的食材信息（用于食谱创建）
class SimpleIngredient(BaseModel):
    name: str = Field(..., min_length=1, description="食材名称")
    quantity: float = Field(..., gt=0, description="数量")
    unit: Optional[str] = Field(None, description="单位")

# 食谱基础模型
class RecipeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="标题")
    description: Optional[str] = Field(None, description="描述")
    cooking_time: int = Field(..., gt=0, description="烹饪时间(分钟)")
    servings: int = Field(..., gt=0, description="份量")
    difficulty: str = Field(..., description="难度")
    ingredients: Optional[List[SimpleIngredient]] = Field(None, description="食材列表")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    image_url: Optional[str] = Field(None, description="图片URL")

# 食谱创建模型
class RecipeCreate(RecipeBase):
    instructions: str = Field(..., min_length=1, description="烹饪步骤")
    nutrition_info: Optional[NutritionInfoBase] = Field(None, description="营养信息")

# 食谱更新模型
class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="标题")
    description: Optional[str] = Field(None, description="描述")
    instructions: Optional[str] = Field(None, min_length=1, description="烹饪步骤")
    cooking_time: Optional[int] = Field(None, gt=0, description="烹饪时间(分钟)")
    servings: Optional[int] = Field(None, gt=0, description="份量")
    difficulty: Optional[str] = Field(None, description="难度")
    ingredients: Optional[List[SimpleIngredient]] = Field(None, description="食材列表")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    image_url: Optional[str] = Field(None, description="图片URL")
    nutrition_info: Optional[NutritionInfoBase] = Field(None, description="营养信息")

# 食谱响应模型
class RecipeResponse(RecipeBase):
    recipe_id: str = Field(..., description="食谱ID")
    author_id: str = Field(..., description="作者ID")
    author_name: Optional[str] = Field(None, description="作者名称")
    instructions: str = Field(..., description="烹饪步骤")
    nutrition_info: Optional[NutritionInfoResponse] = Field(None, description="营养信息")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True

# 食谱列表项模型（简化版）
class RecipeListItem(BaseModel):
    recipe_id: str = Field(..., description="食谱ID")
    title: str = Field(..., description="标题")
    description: Optional[str] = Field(None, description="描述")
    cooking_time: int = Field(..., description="烹饪时间(分钟)")
    difficulty: str = Field(..., description="难度")
    author_name: Optional[str] = Field(None, description="作者名称")
    image_url: Optional[str] = Field(None, description="图片URL")
    created_at: datetime = Field(..., description="创建时间")
    
    class Config:
        from_attributes = True

# 食谱搜索参数模型
class RecipeSearchParams(BaseModel):
    query: Optional[str] = Field(None, description="搜索关键词")
    tags: Optional[List[str]] = Field(None, description="标签筛选")
    difficulty: Optional[str] = Field(None, description="难度筛选")
    max_cooking_time: Optional[int] = Field(None, gt=0, description="最大烹饪时间")
    ingredients_include: Optional[List[str]] = Field(None, description="必须包含的食材")
    ingredients_exclude: Optional[List[str]] = Field(None, description="排除的食材")

# 收藏响应模型
class FavoriteResponse(BaseModel):
    favorite_id: str = Field(..., description="收藏ID")
    user_id: str = Field(..., description="用户ID")
    recipe_id: str = Field(..., description="食谱ID")
    recipe: Optional[RecipeListItem] = Field(None, description="食谱信息")
    created_at: datetime = Field(..., description="收藏时间")
    
    class Config:
        from_attributes = True

# 评分基础模型
class RatingBase(BaseModel):
    score: int = Field(..., ge=1, le=5, description="评分(1-5)")
    comment: Optional[str] = Field(None, description="评论")

# 评分创建模型
class RatingCreate(RatingBase):
    recipe_id: str = Field(..., description="食谱ID")

# 评分响应模型
class RatingResponse(RatingBase):
    rating_id: int = Field(..., description="评分ID")
    user_id: str = Field(..., description="用户ID")
    recipe_id: str = Field(..., description="食谱ID")
    user_name: Optional[str] = Field(None, description="用户名称")
    created_at: datetime = Field(..., description="评分时间")
    
    class Config:
        from_attributes = True