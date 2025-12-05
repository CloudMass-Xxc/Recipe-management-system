#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端到端测试收藏功能的完整性

测试流程：
1. 用户注册（如果用户不存在）
2. 用户登录获取访问令牌
3. 收藏一个食谱
4. 获取用户收藏列表，验证收藏成功
5. 取消收藏
6. 再次获取用户收藏列表，验证取消收藏成功
"""

import requests
import json
import sys
import uuid

# API基础URL
BASE_URL = "http://localhost:8002"
REGISTER_URL = f"{BASE_URL}/api/auth/register"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
RECIPES_URL = f"{BASE_URL}/api/recipes"
FAVORITE_URL = lambda recipe_id: f"{BASE_URL}/api/recipes/{recipe_id}/favorite"
USER_FAVORITES_URL = f"{BASE_URL}/api/recipes/user/favorites"

# 测试用户凭据
USER_CREDENTIALS = {
    "username": f"testuser_{uuid.uuid4().hex[:8]}",
    "email": f"testuser_{uuid.uuid4().hex[:8]}@example.com",
    "password": "password123"
}

# 测试用的食谱ID（将从API获取）
TEST_RECIPE_ID = None


def test_register():
    """测试用户注册"""
    print("📝 步骤1：用户注册")
    print(f"   注册URL: {REGISTER_URL}")
    print(f"   用户名: {USER_CREDENTIALS['username']}")
    print(f"   邮箱: {USER_CREDENTIALS['email']}")
    print(f"   密码: {'*' * len(USER_CREDENTIALS['password'])}")
    
    try:
        # 准备注册数据
        register_data = {
            "username": USER_CREDENTIALS["username"],
            "email": USER_CREDENTIALS["email"],
            "password": USER_CREDENTIALS["password"]
        }
        
        register_response = requests.post(REGISTER_URL, json=register_data)
        print(f"   注册响应状态码: {register_response.status_code}")
        
        if register_response.status_code == 200:
            register_data = register_response.json()
            print(f"   ✅ 注册成功！")
            print(f"   注册响应: {json.dumps(register_data, indent=2, ensure_ascii=False)}")
            return True
        elif register_response.status_code == 400:
            error_data = register_response.json()
            print(f"   ⚠️  注册失败: {error_data['error']['message']}")
            # 如果用户名或邮箱已存在，我们仍然可以尝试登录
            if "用户名已存在" in error_data['error']['message'] or "邮箱已被注册" in error_data['error']['message']:
                print(f"   💡 尝试使用现有用户登录")
                return True
            return False
        else:
            print(f"   ❌ 注册失败: {register_response.status_code}")
            try:
                error_data = register_response.json()
                print(f"   错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   响应内容: {register_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ 注册请求异常: {str(e)}")
        return False


def test_login():
    """测试用户登录并获取访问令牌"""
    print("🔐 步骤2：用户登录")
    print(f"   登录URL: {LOGIN_URL}")
    print(f"   用户名: {USER_CREDENTIALS['username']}")
    print(f"   密码: {'*' * len(USER_CREDENTIALS['password'])}")
    
    try:
        login_response = requests.post(LOGIN_URL, json=USER_CREDENTIALS)
        print(f"   登录响应状态码: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            # access_token 是在 data 字段下面的
            data = login_data.get('data')
            access_token = data.get('access_token') if data else None
            
            if access_token:
                print(f"   ✅ 登录成功！获取到令牌（前20位）: {access_token[:20]}...")
                return access_token
            else:
                print("   ❌ 登录成功，但未获取到访问令牌")
                print(f"   登录响应内容: {json.dumps(login_data, indent=2, ensure_ascii=False)}")
                return None
        else:
            print(f"   ❌ 登录失败: {login_response.status_code}")
            try:
                error_data = login_response.json()
                print(f"   错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   响应内容: {login_response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ 登录请求异常: {str(e)}")
        return None


def test_favorite_recipe(access_token, recipe_id):
    """测试收藏食谱功能"""
    print(f"\n⭐ 步骤3：收藏食谱")
    print(f"   收藏URL: {RECIPES_URL}/{recipe_id}/favorite")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        favorite_response = requests.post(f"{RECIPES_URL}/{recipe_id}/favorite", headers=headers)
        print(f"   收藏响应状态码: {favorite_response.status_code}")
        
        if favorite_response.status_code == 200:
            favorite_data = favorite_response.json()
            print(f"   ✅ 收藏成功！")
            print(f"   收藏响应: {json.dumps(favorite_data, indent=2)}")
            return True
        elif favorite_response.status_code == 400 and "Already favorited" in favorite_response.text:
            print(f"   ⚠️  食谱已经被收藏过")
            return True
        else:
            print(f"   ❌ 收藏失败: {favorite_response.status_code}")
            try:
                error_data = favorite_response.json()
                print(f"   错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   响应内容: {favorite_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ 收藏请求异常: {str(e)}")
        return False


def test_get_user_favorites(access_token):
    """测试获取用户收藏列表功能"""
    print(f"\n📋 步骤4：获取用户收藏列表")
    print(f"   获取收藏URL: {USER_FAVORITES_URL}")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        favorites_response = requests.get(USER_FAVORITES_URL, headers=headers)
        print(f"   获取收藏响应状态码: {favorites_response.status_code}")
        
        if favorites_response.status_code == 200:
            favorites_data = favorites_response.json()
            print(f"   ✅ 获取收藏列表成功！")
            print(f"   收藏数据: {json.dumps(favorites_data, indent=2, ensure_ascii=False)}")
            
            # 检查返回的数据结构
            if isinstance(favorites_data, dict) and 'recipes' in favorites_data:
                recipes = favorites_data['recipes']
                print(f"   收藏食谱数量: {len(recipes)}")
                return recipes
            else:
                print("   ❌ 收藏数据结构不正确")
                return []
        else:
            print(f"   ❌ 获取收藏列表失败: {favorites_response.status_code}")
            try:
                error_data = favorites_response.json()
                print(f"   错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   响应内容: {favorites_response.text}")
            return []
            
    except Exception as e:
        print(f"   ❌ 获取收藏列表请求异常: {str(e)}")
        return []


def test_unfavorite_recipe(access_token, recipe_id):
    """测试取消收藏食谱功能"""
    print(f"\n❌ 步骤5：取消收藏食谱")
    print(f"   取消收藏URL: {RECIPES_URL}/{recipe_id}/favorite")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        unfavorite_response = requests.delete(f"{RECIPES_URL}/{recipe_id}/favorite", headers=headers)
        print(f"   取消收藏响应状态码: {unfavorite_response.status_code}")
        
        if unfavorite_response.status_code == 200:
            unfavorite_data = unfavorite_response.json()
            print(f"   ✅ 取消收藏成功！")
            print(f"   取消收藏响应: {json.dumps(unfavorite_data, indent=2)}")
            return True
        else:
            print(f"   ❌ 取消收藏失败: {unfavorite_response.status_code}")
            try:
                error_data = unfavorite_response.json()
                print(f"   错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   响应内容: {unfavorite_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ 取消收藏请求异常: {str(e)}")
        return False


def get_recipe_id(access_token):
    """从API获取一个存在的食谱ID"""
    print("\n🔍 步骤2.5：获取食谱列表")
    print(f"   获取食谱URL: {RECIPES_URL}")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        # 获取食谱列表 - 不需要认证
        recipes_response = requests.get(RECIPES_URL, headers={"Content-Type": "application/json"}, params={"skip": 0, "limit": 1})
        print(f"   获取食谱响应状态码: {recipes_response.status_code}")
        
        if recipes_response.status_code == 200:
            recipes_data = recipes_response.json()
            
            # 检查响应数据结构
            if isinstance(recipes_data, dict) and 'recipes' in recipes_data:
                recipes = recipes_data['recipes']
                if recipes:
                    recipe_id = recipes[0].get('recipe_id')
                    recipe_title = recipes[0].get('title')
                    print(f"   ✅ 获取到食谱ID: {recipe_id}")
                    print(f"   食谱标题: {recipe_title}")
                    return recipe_id
                else:
                    print("   ❌ 食谱列表为空")
                    # 如果食谱列表为空，尝试创建一个新食谱
                    return create_test_recipe(access_token)
            else:
                print("   ❌ 食谱数据结构不正确")
                print(f"   响应数据: {json.dumps(recipes_data, indent=2, ensure_ascii=False)}")
                return None
        else:
            print(f"   ❌ 获取食谱列表失败: {recipes_response.status_code}")
            try:
                error_data = recipes_response.json()
                print(f"   错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   响应内容: {recipes_response.text}")
            # 如果获取食谱列表失败，尝试创建一个新食谱
            return create_test_recipe(access_token)
            
    except Exception as e:
        print(f"   ❌ 获取食谱列表请求异常: {str(e)}")
        # 如果请求异常，尝试创建一个新食谱
        return create_test_recipe(access_token)

def create_test_recipe(access_token):
    """创建一个测试用的食谱"""
    print("\n📝 步骤2.6：创建测试食谱")
    print(f"   创建食谱URL: {RECIPES_URL}")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 测试食谱数据
    recipe_data = {
        "title": "测试收藏功能的食谱",
        "description": "这是一个用于测试收藏功能的食谱",
        "difficulty": "easy",
        "cooking_time": 30,
        "prep_time": 15,
        "servings": 2,
        "instructions": "准备食材\n烹饪\n享用",
        "ingredients": [
            {"name": "鸡蛋", "quantity": 2, "unit": "个"},
            {"name": "米饭", "quantity": 1, "unit": "碗"}
        ],
        "tags": ["测试", "收藏"]
    }
    
    try:
        # 创建食谱
        create_response = requests.post(RECIPES_URL, headers=headers, json=recipe_data)
        print(f"   创建食谱响应状态码: {create_response.status_code}")
        
        if create_response.status_code == 200:
            create_data = create_response.json()
            recipe_id = create_data.get('recipe_id')
            if recipe_id:
                print(f"   ✅ 创建食谱成功，食谱ID: {recipe_id}")
                print(f"   食谱标题: {recipe_data['title']}")
                return recipe_id
            else:
                print("   ❌ 创建食谱成功，但未获取到食谱ID")
                print(f"   响应数据: {json.dumps(create_data, indent=2, ensure_ascii=False)}")
                return None
        else:
            print(f"   ❌ 创建食谱失败: {create_response.status_code}")
            try:
                error_data = create_response.json()
                print(f"   错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   响应内容: {create_response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ 创建食谱请求异常: {str(e)}")
        return None


def test_favorite_functionality():
    """测试收藏功能的完整流程"""
    print("开始测试收藏功能的完整流程...\n")
    global TEST_RECIPE_ID
    
    try:
        # 步骤1：用户注册
        register_success = test_register()
        if not register_success:
            print("\n❌ 注册失败，测试终止")
            return False
        
        # 步骤2：用户登录
        access_token = test_login()
        if not access_token:
            print("\n❌ 登录失败，测试终止")
            return False
        
        # 步骤2.5：获取一个存在的食谱ID
        TEST_RECIPE_ID = get_recipe_id(access_token)
        if not TEST_RECIPE_ID:
            print("\n❌ 获取食谱ID失败，测试终止")
            return False
        
        # 步骤3：收藏食谱
        favorite_success = test_favorite_recipe(access_token, TEST_RECIPE_ID)
        if not favorite_success:
            print("\n❌ 收藏食谱失败，测试终止")
            return False
        
        # 步骤4：获取用户收藏列表
        favorites = test_get_user_favorites(access_token)
        if not favorites:
            print("\n❌ 获取收藏列表失败或收藏列表为空，测试终止")
            return False
        
        # 验证收藏的食谱在列表中
        target_recipe = next((recipe for recipe in favorites if recipe['recipe_id'] == TEST_RECIPE_ID), None)
        if target_recipe:
            print(f"\n✅ 验证成功：食谱 {TEST_RECIPE_ID} 在收藏列表中")
            print(f"   食谱标题: {target_recipe.get('title')}")
        else:
            print(f"\n❌ 验证失败：食谱 {TEST_RECIPE_ID} 不在收藏列表中")
            return False
        
        # 步骤5：取消收藏
        unfavorite_success = test_unfavorite_recipe(access_token, TEST_RECIPE_ID)
        if not unfavorite_success:
            print("\n❌ 取消收藏失败，测试终止")
            return False
        
        # 步骤6：再次获取用户收藏列表，验证取消收藏成功
        updated_favorites = test_get_user_favorites(access_token)
        updated_target_recipe = next((recipe for recipe in updated_favorites if recipe['recipe_id'] == TEST_RECIPE_ID), None)
        
        if not updated_target_recipe:
            print(f"\n✅ 验证成功：食谱 {TEST_RECIPE_ID} 已从收藏列表中移除")
        else:
            print(f"\n❌ 验证失败：食谱 {TEST_RECIPE_ID} 仍然在收藏列表中")
            return False
        
        print("\n🎉 收藏功能的完整流程测试成功！")
        return True
        
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        return False
    except Exception as e:
        print(f"\n❌ 测试过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_favorite_functionality()
    sys.exit(0 if success else 1)
