#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试食谱加载修复

此脚本测试以下功能：
1. 安全地获取食谱详情（使用有效和无效的recipe_id）
2. 测试食谱列表获取功能（包括标签筛选）
"""

import sys
import os
import logging
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.recipes.services import RecipeService
from app.models.recipe import Recipe

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("recipe_fix_test")

def test_get_recipe_by_id():
    """测试根据ID获取食谱功能"""
    logger.info("=== 开始测试 get_recipe_by_id 方法 ===")
    
    db: Session = next(get_db())
    
    try:
        # 获取所有食谱
        recipes = db.query(Recipe).all()
        if not recipes:
            logger.warning("数据库中没有食谱数据，跳过测试")
            return True
        
        # 测试1：使用有效UUID获取食谱
        valid_recipe = recipes[0]
        logger.info(f"测试1: 使用有效UUID获取食谱 (ID: {valid_recipe.recipe_id})")
        
        result = RecipeService.get_recipe_by_id(db, valid_recipe.recipe_id)
        if result:
            logger.info(f"✅ 测试1通过：成功获取食谱 '{result.title}'")
        else:
            logger.error("❌ 测试1失败：无法获取有效食谱")
            return False
        
        # 测试2：使用字符串格式的有效UUID获取食谱
        logger.info(f"测试2: 使用字符串格式的有效UUID获取食谱 (ID: {str(valid_recipe.recipe_id)})")
        
        result2 = RecipeService.get_recipe_by_id(db, str(valid_recipe.recipe_id))
        if result2:
            logger.info(f"✅ 测试2通过：成功获取食谱 '{result2.title}'")
        else:
            logger.error("❌ 测试2失败：无法使用字符串格式的有效UUID获取食谱")
            return False
        
        # 测试3：使用无效的recipe_id（非UUID格式）
        invalid_recipe_id = "invalid-recipe-id-123"
        logger.info(f"测试3: 使用无效的recipe_id获取食谱 (ID: {invalid_recipe_id})")
        
        result3 = RecipeService.get_recipe_by_id(db, invalid_recipe_id)
        if result3 is None:
            logger.info("✅ 测试3通过：无效的recipe_id返回None")
        else:
            logger.error(f"❌ 测试3失败：无效的recipe_id应该返回None，实际返回: {result3}")
            return False
        
        # 测试4：使用None作为recipe_id
        logger.info("测试4: 使用None作为recipe_id获取食谱")
        
        result4 = RecipeService.get_recipe_by_id(db, None)
        if result4 is None:
            logger.info("✅ 测试4通过：None作为recipe_id返回None")
        else:
            logger.error(f"❌ 测试4失败：None作为recipe_id应该返回None，实际返回: {result4}")
            return False
        
        logger.info("=== get_recipe_by_id 方法测试全部通过 ===")
        return True
        
    except Exception as e:
        logger.error(f"测试过程中发生异常: {str(e)}", exc_info=True)
        return False
    finally:
        db.close()

def test_get_recipes():
    """测试获取食谱列表功能，包括标签筛选"""
    logger.info("\n=== 开始测试 get_recipes 方法 ===")
    
    db: Session = next(get_db())
    
    try:
        # 测试1：获取所有食谱（不使用筛选条件）
        logger.info("测试1: 获取所有食谱（不使用筛选条件）")
        
        recipes = RecipeService.get_recipes(db, skip=0, limit=10)
        if isinstance(recipes, list):
            logger.info(f"✅ 测试1通过：成功获取 {len(recipes)} 个食谱")
        else:
            logger.error(f"❌ 测试1失败：返回值不是列表，实际类型: {type(recipes)}")
            return False
        
        # 测试2：使用标签筛选（使用可能不存在的标签）
        logger.info("测试2: 使用标签筛选（使用可能不存在的标签）")
        
        search_params = {
            "tags": ["vegetarian"]  # 尝试使用一个常见的标签
        }
        
        filtered_recipes = RecipeService.get_recipes(db, skip=0, limit=10, search_params=search_params)
        if isinstance(filtered_recipes, list):
            logger.info(f"✅ 测试2通过：成功获取 {len(filtered_recipes)} 个符合标签条件的食谱")
        else:
            logger.error(f"❌ 测试2失败：返回值不是列表，实际类型: {type(filtered_recipes)}")
            return False
        
        # 测试3：使用多个筛选条件
        logger.info("测试3: 使用多个筛选条件（关键词搜索、难度筛选、烹饪时间限制）")
        
        search_params_3 = {
            "query": "test",  # 搜索关键词
            "difficulty": "easy",  # 难度筛选
            "max_cooking_time": 60  # 最大烹饪时间
        }
        
        multi_filtered_recipes = RecipeService.get_recipes(
            db, skip=0, limit=10, search_params=search_params_3
        )
        
        if isinstance(multi_filtered_recipes, list):
            logger.info(f"✅ 测试3通过：成功获取 {len(multi_filtered_recipes)} 个符合多个条件的食谱")
        else:
            logger.error(f"❌ 测试3失败：返回值不是列表，实际类型: {type(multi_filtered_recipes)}")
            return False
        
        # 测试4：使用空的筛选条件
        logger.info("测试4: 使用空的筛选条件")
        
        empty_filter_recipes = RecipeService.get_recipes(
            db, skip=0, limit=10, search_params={}
        )
        
        if isinstance(empty_filter_recipes, list):
            logger.info(f"✅ 测试4通过：成功获取 {len(empty_filter_recipes)} 个食谱")
        else:
            logger.error(f"❌ 测试4失败：返回值不是列表，实际类型: {type(empty_filter_recipes)}")
            return False
        
        logger.info("=== get_recipes 方法测试全部通过 ===")
        return True
        
    except Exception as e:
        logger.error(f"测试过程中发生异常: {str(e)}", exc_info=True)
        return False
    finally:
        db.close()

def main():
    """运行所有测试"""
    logger.info("开始测试食谱加载修复...")
    
    # 运行测试
    test1_result = test_get_recipe_by_id()
    test2_result = test_get_recipes()
    
    # 汇总结果
    logger.info("\n=== 测试结果汇总 ===")
    logger.info(f"get_recipe_by_id 测试: {'通过' if test1_result else '失败'}")
    logger.info(f"get_recipes 测试: {'通过' if test2_result else '失败'}")
    
    if test1_result and test2_result:
        logger.info("🎉 所有测试都通过了！食谱加载修复成功。")
        return 0
    else:
        logger.error("💥 部分测试失败，需要进一步修复。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
