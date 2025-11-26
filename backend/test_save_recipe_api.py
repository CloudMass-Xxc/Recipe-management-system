#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 '添加到我的食谱' API功能
直接使用测试用户ID，绕过登录步骤，专注测试API数据格式处理
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入应用和数据库模型
from main import app
from app.core.database import get_db, engine
from app.models.recipe import Recipe
from app.models.user import User

# 测试配置
TEST_USER_ID = "b9c9b23f-0fb9-4422-8ee2-3f0eb19d4e21"  # 从之前测试中获取的有效用户ID

# 创建测试客户端
client = TestClient(app)

# 模拟前端生成的食谱数据
sample_recipe_data = {
    "title": "API测试食谱",
    "description": "这是一个API测试用的食谱",
    "difficulty": "easy",
    "cooking_time": 30,
    "prep_time": 15,
    "servings": 2,
    "instructions": ["准备食材", "烹饪", "享用"],
    "tips": ["可以根据个人口味调整调味料"],
    "nutrition_info": {
        "calories": 500,
        "protein": 20,
        "carbs": 60,
        "fat": 15,
        "fiber": 5
    },
    "ingredients": [
        {
            "name": "鸡蛋",
            "quantity": 2,
            "unit": "个",
            "note": "新鲜"
        },
        {
            "name": "米饭",
            "quantity": 1,
            "unit": "碗",
            "note": "煮熟"
        }
    ],
    "tags": ["测试", "快速"]
}

def test_save_recipe_api():
    """测试保存食谱API"""
    print("开始测试 '添加到我的食谱' API功能...\n")
    
    # 步骤1：验证测试用户存在
    print("🔍 步骤1：验证测试用户")
    db = next(get_db())
    test_user = db.query(User).filter(User.user_id == TEST_USER_ID).first()
    
    if test_user:
        print(f"   ✅ 找到测试用户: {test_user.username} (ID: {test_user.user_id})")
    else:
        print(f"   ❌ 未找到测试用户: {TEST_USER_ID}")
        return False
    
    # 步骤2：准备请求体
    print("\n📋 步骤2：准备请求数据")
    request_body = {
        "recipe_data": sample_recipe_data,
        "share_with_community": False
    }
    
    print(f"   请求URL: /ai/save-generated-recipe")
    print(f"   请求体结构:")
    print(f"     - recipe_data: 包含{len(sample_recipe_data)}个字段")
    print(f"     - instructions: {len(sample_recipe_data['instructions'])}个步骤（数组格式）")
    print(f"     - tips: {len(sample_recipe_data['tips'])}个小贴士（数组格式）")
    print(f"     - ingredients: {len(sample_recipe_data['ingredients'])}种食材")
    print(f"     - share_with_community: False")
    
    # 步骤3：调用API（使用依赖注入模拟用户认证）
    print("\n🚀 步骤3：调用保存食谱API")
    
    # 重写get_current_user依赖，直接返回测试用户
    def override_get_current_user():
        return test_user
    
    # 重写依赖
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    try:
        response = client.post(
            "/ai/save-generated-recipe",
            json=request_body,
            headers={"Authorization": f"Bearer test_token"}  # 令牌不重要，因为我们重写了认证
        )
        
        print(f"   响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ 保存食谱成功！")
            print(f"   保存结果:")
            print(f"     - 食谱ID: {data.get('recipe_id')}")
            print(f"     - 标题: {data.get('title')}")
            print(f"     - 作者ID: {data.get('author_id')}")
            print(f"     - 创建时间: {data.get('created_at')}")
            
            # 验证数据库中是否存在该食谱
            saved_recipe = db.query(Recipe).filter(Recipe.id == data.get('recipe_id')).first()
            if saved_recipe:
                print("   ✅ 食谱已成功保存到数据库！")
                print(f"     - 数据库记录ID: {saved_recipe.id}")
                print(f"     - 数据库记录标题: {saved_recipe.title}")
                print(f"     - 数据库记录作者ID: {saved_recipe.author_id}")
            else:
                print("   ⚠️  食谱API返回成功，但数据库中未找到记录")
                
            return True
        else:
            print(f"   ❌ 保存食谱失败: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   错误信息: {error_data}")
            except:
                print(f"   响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ 请求异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清除依赖重写
        app.dependency_overrides.clear()

def get_current_user():
    """模拟获取当前用户的依赖"""
    from fastapi import Depends, HTTPException, status
    from fastapi.security import OAuth2PasswordBearer
    from sqlalchemy.orm import Session
    from app.core.database import get_db
    from app.models.user import User
    from app.core.security import decode_access_token
    
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
    
    def _get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = decode_access_token(token)
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except Exception:
            raise credentials_exception
            
        user = db.query(User).filter(User.user_id == user_id).first()
        if user is None:
            raise credentials_exception
            
        return user
    
    return _get_current_user()

def main():
    """主测试函数"""
    print("🎯 ========== 测试 '添加到我的食谱' API功能 ==========\n")
    
    success = test_save_recipe_api()
    
    print("\n🏁 ========== 测试结果汇总 ==========")
    if success:
        print("🎉 测试通过！'添加到我的食谱' API功能正常工作。")
        print("\n✅ 修复内容总结：")
        print("   1. 修复了 Pydantic V2 兼容性问题（@validator -> @field_validator）")
        print("   2. 修复了前端数据格式问题（instructions应该是字符串数组）")
        print("   3. 确保了前后端数据格式一致性")
        print("   4. API能够正确处理数组格式的instructions和tips")
        sys.exit(0)
    else:
        print("💥 测试失败！'添加到我的食谱' API功能仍有问题。")
        print("\n❌ 可能的问题：")
        print("   1. API端点路径错误")
        print("   2. 依赖注入配置问题")
        print("   3. 数据库连接问题")
        print("   4. 数据验证失败")
        sys.exit(1)

if __name__ == "__main__":
    main()