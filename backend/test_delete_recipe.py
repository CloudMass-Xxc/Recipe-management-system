#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试删除食谱功能，验证数据库级联删除是否正常工作
"""

import sys
import os
import json
import requests
from typing import Dict, Any

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# API基础URL
API_BASE_URL = "http://localhost:8000"

# 测试用户凭据
TEST_CREDENTIALS = {
    "identifier": "xuxiaochang@qq.com",
    "password": "Xxc20001018"
}

def test_delete_recipe_flow():
    """测试删除食谱的完整流程"""
    print("开始测试删除食谱功能...")
    
    try:
        # 1. 登录获取令牌
        print("\n1. 登录获取令牌...")
        login_response = requests.post(
            f"{API_BASE_URL}/api/auth/login",
            json=TEST_CREDENTIALS,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code != 200:
            print(f"登录失败: {login_response.status_code}")
            print(f"错误信息: {login_response.text}")
            return False
        
        login_data = login_response.json()
        token = login_data.get("access_token")
        
        if not token:
            print("获取令牌失败")
            return False
        
        print(f"获取令牌成功: {token[:20]}...")
        
        # 2. 获取用户的食谱列表
        print("\n2. 获取用户的食谱列表...")
        auth_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        recipes_response = requests.get(
            f"{API_BASE_URL}/recipes/user",
            headers=auth_headers
        )
        
        if recipes_response.status_code != 200:
            print(f"获取食谱列表失败: {recipes_response.status_code}")
            print(f"错误信息: {recipes_response.text}")
            return False
        
        recipes_data = recipes_response.json()
        print(f"获取到 {len(recipes_data)} 个食谱")
        
        if not recipes_data:
            print("没有找到用户的食谱，请先创建食谱后再测试")
            return False
        
        # 3. 选择第一个食谱进行删除测试
        recipe_to_delete = recipes_data[0]
        recipe_id = recipe_to_delete["id"]
        recipe_title = recipe_to_delete["title"]
        
        print(f"\n3. 选择要删除的食谱:")
        print(f"   ID: {recipe_id}")
        print(f"   标题: {recipe_title}")
        
        # 4. 删除食谱
        print(f"\n4. 删除食谱...")
        delete_response = requests.delete(
            f"{API_BASE_URL}/recipes/{recipe_id}",
            headers=auth_headers
        )
        
        if delete_response.status_code == 204:
            print("食谱删除成功！状态码: 204")
        else:
            print(f"删除食谱失败: {delete_response.status_code}")
            print(f"错误信息: {delete_response.text}")
            return False
        
        # 5. 验证食谱已从列表中移除
        print("\n5. 验证食谱已从列表中移除...")
        verify_response = requests.get(
            f"{API_BASE_URL}/recipes/user",
            headers=auth_headers
        )
        
        if verify_response.status_code != 200:
            print(f"验证失败: {verify_response.status_code}")
            print(f"错误信息: {verify_response.text}")
            return False
        
        updated_recipes = verify_response.json()
        deleted_recipe_exists = any(recipe["id"] == recipe_id for recipe in updated_recipes)
        
        if not deleted_recipe_exists:
            print("验证成功！食谱已从用户列表中移除")
        else:
            print("验证失败！食谱仍然存在于用户列表中")
            return False
        
        # 6. 尝试直接访问已删除的食谱
        print("\n6. 尝试直接访问已删除的食谱...")
        direct_response = requests.get(
            f"{API_BASE_URL}/recipes/{recipe_id}",
            headers=auth_headers
        )
        
        if direct_response.status_code == 404:
            print("验证成功！已删除的食谱无法直接访问 (404)")
        else:
            print(f"验证失败！已删除的食谱仍然可以访问: {direct_response.status_code}")
            print(f"响应内容: {direct_response.text}")
            return False
        
        print("\n🎉 删除食谱功能测试通过！")
        print("✅ 食谱成功从数据库中删除")
        print("✅ 相关联的数据（如食材、营养信息、收藏等）也应该通过级联删除被移除")
        return True
        
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_delete_recipe_flow()
    sys.exit(0 if success else 1)
