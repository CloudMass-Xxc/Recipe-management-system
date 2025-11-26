# -*- coding: utf-8 -*-
"""
简化的食谱保存测试脚本 - 详细日志版
"""

from app.core.database import get_db, Base
from app.models.recipe import Recipe
from app.models.user import User
from app.models.nutrition_info import NutritionInfo
from app.models.ingredient import Ingredient
from app.models.recipe_ingredient import RecipeIngredient
from app.recipes.services import RecipeService
from sqlalchemy.exc import SQLAlchemyError
import uuid
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_save_recipe():
    """
    测试保存食谱功能
    """
    try:
        # 获取数据库会话
        db = next(get_db())
        logger.info("获取数据库会话成功")
        
        # 确保有一个用户用于测试
        user = db.query(User).first()
        if not user:
            user = User(
                user_id=str(uuid.uuid4()),
                username="testuser",
                email="test@example.com",
                password_hash="hashed_password",
                is_active=True
            )
            db.add(user)
            db.commit()
            logger.info("创建测试用户成功")
        else:
            logger.info(f"使用现有测试用户: {user.username}")
        
        # 准备食谱数据
        recipe_data = {
            "title": "测试食谱",
            "description": "这是一个测试用的食谱",
            "difficulty": "easy",
            "cooking_time": 30,
            "prep_time": 10,
            "servings": 2,
            "instructions": "准备食材\n烹饪\n享用",
            "nutrition_info": {
                "calories": 500,
                "protein": 20,
                "carbs": 60,
                "fat": 15,
                "fiber": 5
            },
            "ingredients": [
                {"name": "鸡蛋", "quantity": 2, "unit": "个"},
                {"name": "米饭", "quantity": 1, "unit": "碗"}
            ],
            "tags": ["测试", "快速"]
        }
        
        logger.info("准备食谱数据成功")
        logger.debug(f"食谱数据: {recipe_data}")
        
        # 尝试创建食谱
        logger.info("开始创建食谱...")
        new_recipe = RecipeService.create_recipe(db, user.user_id, recipe_data)
        logger.info(f"创建食谱成功! 食谱ID: {new_recipe.recipe_id}")
        
        # 尝试获取完整的食谱数据（包括关联数据）
        logger.info("开始获取完整食谱数据...")
        full_recipe = RecipeService.get_recipe_by_id(db, new_recipe.recipe_id)
        
        if full_recipe:
            logger.info("获取完整食谱数据成功!")
            logger.info(f"食谱标题: {full_recipe.title}")
            logger.info(f"食谱作者: {full_recipe.author.username}")
            
            # 检查营养信息
            if full_recipe.nutrition_info:
                logger.info("营养信息:")
                logger.info(f"  卡路里: {full_recipe.nutrition_info.calories}")
                logger.info(f"  蛋白质: {full_recipe.nutrition_info.protein}")
                logger.info(f"  碳水化合物: {full_recipe.nutrition_info.carbs}")
                logger.info(f"  脂肪: {full_recipe.nutrition_info.fat}")
                logger.info(f"  纤维: {full_recipe.nutrition_info.fiber}")
            else:
                logger.warning("未找到营养信息")
            
            # 检查食材
            if full_recipe.ingredients:
                logger.info("食材列表:")
                for ingredient in full_recipe.ingredients:
                    logger.info(f"  - {ingredient.quantity} {ingredient.unit} {ingredient.ingredient.name}")
            else:
                logger.warning("未找到食材列表")
            
            # 检查标签
            if full_recipe.tags:
                logger.info(f"标签: {full_recipe.tags}")
            else:
                logger.warning("未找到标签")
        else:
            logger.error("获取完整食谱数据失败")
        
        return True
        
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}", exc_info=True)
        import traceback
        logger.error(f"详细错误堆栈: {traceback.format_exc()}")
        return False
    except Exception as e:
        logger.error(f"其他错误: {str(e)}", exc_info=True)
        import traceback
        logger.error(f"详细错误堆栈: {traceback.format_exc()}")
        return False
    finally:
        # 关闭数据库会话
        try:
            db.close()
            logger.info("关闭数据库会话成功")
        except:
            pass


if __name__ == "__main__":
    logger.info("开始测试食谱保存功能...")
    success = test_save_recipe()
    if success:
        logger.info("测试成功！食谱保存功能正常工作。")
    else:
        logger.error("测试失败！食谱保存功能存在问题。")
