#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单测试脚本：直接测试RecipeService.create_recipe方法
"""

import sys
import os
from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.recipes.services import RecipeService
from app.models.user import User

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 创建或获取测试用户
def get_or_create_test_user(db: Session) -> User:
    """创建或获取测试用户"""
    # 先尝试查找现有用户
    test_user = db.query(User).filter(User.username == "testuser").first()
    
    if not test_user:
        # 如果不存在，创建新用户
        print("   📝 测试用户不存在，创建新用户...")
        test_user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            display_name="Test User"  # 必需字段
        )
        db.add(test_user)
        db.commit()
        print("   ✅ 新测试用户创建成功")
    else:
        print(f"   ✅ 找到现有测试用户: {test_user.username}")
    
    return test_user

# 主测试函数
def main():
    """主测试函数"""
    print("=== 开始简单测试：RecipeService.create_recipe ===")
    
    try:
        # 获取数据库会话
        db = SessionLocal()
        
        # 创建或获取测试用户
        print("1. 创建或获取测试用户...")
        test_user = get_or_create_test_user(db)
        print(f"   ✅ 测试用户准备完成: {test_user.user_id}")
        
        # 准备简单的食谱数据
        print("2. 准备食谱数据...")
        recipe_data = {
            "title": "测试食谱",
            "description": "这是一个测试用的食谱",
            "difficulty": "easy",
            "cooking_time": 30,
            "servings": 2,
            "instructions": "准备食材\n烹饪\n享用",
            "ingredients": [
                {"name": "鸡蛋", "quantity": 2, "unit": "个", "note": "新鲜"},
                {"name": "米饭", "quantity": 1, "unit": "碗", "note": "煮熟"}
            ],
            "tags": ["测试", "快速"]
        }
        print("   ✅ 食谱数据准备完成")
        
        # 直接调用create_recipe方法
        print("3. 调用create_recipe方法...")
        new_recipe = RecipeService.create_recipe(db, test_user.user_id, recipe_data)
        print(f"   ✅ 食谱创建成功: {new_recipe.recipe_id}")
        
        # 获取保存的食谱
        print("4. 获取保存的食谱...")
        saved_recipe = RecipeService.get_recipe_by_id(db, new_recipe.recipe_id)
        print(f"   ✅ 食谱获取成功: {saved_recipe.title}")
        
        # 打印保存的食谱信息
        print("\n5. 保存的食谱信息：")
        print(f"   ID: {saved_recipe.recipe_id}")
        print(f"   标题: {saved_recipe.title}")
        print(f"   描述: {saved_recipe.description}")
        print(f"   作者ID: {saved_recipe.author_id}")
        print(f"   烹饪时间: {saved_recipe.cooking_time}分钟")
        print(f"   份量: {saved_recipe.servings}")
        print(f"   难度: {saved_recipe.difficulty}")
        print(f"   食材数量: {len(saved_recipe.ingredients) if saved_recipe.ingredients else 0}")
        print(f"   标签数量: {len(saved_recipe.tags) if saved_recipe.tags else 0}")
        
        print("\n=== 测试完成，所有步骤成功！===")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        print("\n详细错误信息:")
        traceback.print_exc()
    finally:
        # 关闭数据库会话
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    main()
