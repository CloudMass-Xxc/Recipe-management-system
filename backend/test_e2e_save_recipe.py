#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
端到端测试 '添加到我的食谱' 功能
模拟前端完整流程：登录 -> 准备数据 -> 调用保存食谱API
"""

import requests
import json
import sys

# 测试配置
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/auth/login"  # 正确的登录URL
SAVE_RECIPE_URL = f"{BASE_URL}/ai/save-generated-recipe"

# 用户凭据（使用用户提供的信息）
USER_CREDENTIALS = {
    "identifier": "xxiaochang@qq.com",
    "password": "Xxc20001018..."
}

# 模拟前端生成的食谱数据
sample_recipe_data = {
    "title": "测试食谱 - 端到端",
    "description": "这是一个端到端测试用的食谱",
    "difficulty": "easy",
    "cooking_time": 30,
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

def test_e2e_save_recipe():
    """端到端测试保存食谱功能"""
    print("开始端到端测试 '添加到我的食谱' 功能...\n")
    
    # 步骤1：登录获取令牌
    print("🔐 步骤1：用户登录")
    print(f"   登录URL: {LOGIN_URL}")
    print(f"   用户名: {USER_CREDENTIALS['identifier']}")
    print(f"   密码: {'*' * len(USER_CREDENTIALS['password'])}")
    
    try:
        login_response = requests.post(LOGIN_URL, json=USER_CREDENTIALS)
        print(f"   登录响应状态码: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            access_token = login_data.get('access_token')
            
            if access_token:
                print(f"   ✅ 登录成功！获取到令牌（前20位）: {access_token[:20]}...")
            else:
                print("   ❌ 登录成功，但未获取到访问令牌")
                print(f"   登录响应内容: {json.dumps(login_data, indent=2)}")
                return False
        else:
            print(f"   ❌ 登录失败: {login_response.status_code}")
            try:
                error_data = login_response.json()
                print(f"   错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   响应内容: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ 登录请求异常: {str(e)}")
        return False
    
    # 步骤2：准备请求头和请求体
    print("\n📋 步骤2：准备请求数据")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 模拟前端recipeAPI.ts中的saveGeneratedRecipe方法处理逻辑
    processed_recipe_data = {
        **sample_recipe_data,
        "instructions": sample_recipe_data["instructions"],
        "tips": sample_recipe_data["tips"]
    }
    
    request_body = {
        "recipe_data": processed_recipe_data,
        "share_with_community": False
    }
    
    print(f"   请求头: Authorization: Bearer {access_token[:20]}...")
    print(f"   请求URL: {SAVE_RECIPE_URL}")
    print(f"   请求体结构:")
    print(f"     - recipe_data: 包含{len(processed_recipe_data)}个字段")
    print(f"     - instructions: {len(processed_recipe_data['instructions'])}个步骤")
    print(f"     - ingredients: {len(processed_recipe_data['ingredients'])}种食材")
    print(f"     - share_with_community: False")
    
    # 步骤3：调用保存食谱API
    print("\n🚀 步骤3：调用保存食谱API")
    try:
        save_response = requests.post(
            SAVE_RECIPE_URL, 
            json=request_body, 
            headers=headers
        )
        
        print(f"   响应状态码: {save_response.status_code}")
        
        if save_response.status_code == 200:
            save_data = save_response.json()
            print("   ✅ 保存食谱成功！")
            print(f"   保存结果:")
            print(f"     - 食谱ID: {save_data.get('recipe_id')}")
            print(f"     - 标题: {save_data.get('title')}")
            print(f"     - 作者ID: {save_data.get('author_id')}")
            print(f"     - 创建时间: {save_data.get('created_at')}")
            return True
        else:
            print(f"   ❌ 保存食谱失败: {save_response.status_code}")
            try:
                error_data = save_response.json()
                print(f"   错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   响应内容: {save_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ 请求异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🎯 ========== 端到端测试 '添加到我的食谱' 功能 ==========\n")
    
    success = test_e2e_save_recipe()
    
    print("\n🏁 ========== 测试结果汇总 ==========")
    if success:
        print("🎉 测试通过！'添加到我的食谱' 功能正常工作。")
        print("\n✅ 修复内容总结：")
        print("   1. 修复了 Pydantic V2 兼容性问题（@validator -> @field_validator）")
        print("   2. 修复了前端数据格式问题（instructions应该是字符串数组）")
        print("   3. 确保了前后端数据格式一致性")
        sys.exit(0)
    else:
        print("💥 测试失败！'添加到我的食谱' 功能仍有问题。")
        sys.exit(1)

if __name__ == "__main__":
    main()
