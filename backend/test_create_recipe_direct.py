#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接测试RecipeService.create_recipe方法的核心功能
不涉及HTTP请求和认证，直接调用服务层方法
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import engine, Base
from app.models.user import User
from app.recipes.services import RecipeService
from app.core.database import get_db

# 创建测试数据库会话
db = next(get_db())

def test_create_recipe_direct():
    """直接测试RecipeService.create_recipe方法"""
    print("开始直接测试 RecipeService.create_recipe 方法...\n")
    
    try:
        # 获取一个测试用户（使用第一个用户）
        test_user = db.query(User).first()
        if not test_user:
            print("❌ 没有找到测试用户，请先注册一个用户。")
            return False
        
        print(f"找到测试用户: {test_user.username} (ID: {test_user.user_id})")
        
        # 准备测试食谱数据
        recipe_data = {
            "title": "直接测试食谱",
            "description": "这是一个直接测试用的食谱",
            "difficulty": "easy",
            "cooking_time": 30,
            "prep_time": 15,
            "servings": 2,
            "instructions": "准备食材\n烹饪\n享用",
            "ingredients": [
                {"name": "鸡蛋", "quantity": 2, "unit": "个", "note": "新鲜"},
                {"name": "米饭", "quantity": 1, "unit": "碗", "note": "煮熟"}
            ],
            "nutrition_info": {
                "calories": 500,
                "protein": 20,
                "carbs": 60,
                "fat": 15,
                "fiber": 5
            },
            "tags": ["测试", "快速"]
        }
        
        print("\n测试食谱数据:")
        print(f"  标题: {recipe_data['title']}")
        print(f"  难度: {recipe_data['difficulty']}")
        print(f"  烹饪时间: {recipe_data['cooking_time']}分钟")
        print(f"  食材数量: {len(recipe_data['ingredients'])}种")
        # 先计算烹饪步骤数量，避免f-string中的反斜杠问题
        instructions_count = len(recipe_data['instructions'].split('\n'))
        print(f"  烹饪步骤: {instructions_count}步")
        
        # 直接调用RecipeService.create_recipe方法
        print("\n调用 RecipeService.create_recipe 方法...")
        new_recipe = RecipeService.create_recipe(db, test_user.user_id, recipe_data)
        
        if new_recipe:
            print("✅ 食谱创建成功！")
            print(f"   食谱ID: {new_recipe.recipe_id}")
            print(f"   标题: {new_recipe.title}")
            print(f"   作者ID: {new_recipe.author_id}")
            print(f"   食材JSON: {new_recipe.ingredients}")
            print(f"   标签JSON: {new_recipe.tags}")
            return True
        else:
            print("❌ 食谱创建失败，返回None。")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 关闭数据库会话
        if db:
            db.close()

if __name__ == "__main__":
    print("========== 直接测试 RecipeService.create_recipe 方法 ==========\n")
    
    success = test_create_recipe_direct()
    
    print("\n========== 测试结果 ==========")
    if success:
        print("🎉 测试通过: RecipeService.create_recipe 方法正常工作！")
        sys.exit(0)
    else:
        print("💥 测试失败: RecipeService.create_recipe 方法存在问题。")
        sys.exit(1)
