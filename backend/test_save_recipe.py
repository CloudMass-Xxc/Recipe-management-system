#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试保存生成食谱功能
"""

import asyncio
import json
import aiohttp

# 配置
base_url = "http://localhost:8000"
login_url = f"{base_url}/auth/login"
save_recipe_url = f"{base_url}/ai/save-generated-recipe"

# 测试用户凭证
email = "xxiaochang@qq.com"
password = "Xxc20001018..."

# 测试用的食谱数据
test_recipe_data = {
    "recipe_data": {
        "title": "测试食谱",
        "description": "这是一个测试用的食谱",
        "difficulty": "easy",
        "cooking_time": 30,
        "prep_time": 10,
        "servings": 2,
        "instructions": ["准备食材", "烹饪", "享用"],
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
    },
    "share_with_community": False
}

async def login():
    """
    登录获取访问令牌
    """
    print("正在登录...")
    async with aiohttp.ClientSession() as session:
        async with session.post(login_url, json={
            "identifier": email,
            "password": password
        }) as response:
            if response.status == 200:
                data = await response.json()
                print("登录成功!")
                return data.get("access_token")
            else:
                print(f"登录失败: {response.status}")
                print(await response.text())
                return None

async def save_recipe(token):
    """
    保存食谱测试
    """
    print("\n正在保存食谱...")
    print(f"请求数据: {json.dumps(test_recipe_data, ensure_ascii=False, indent=2)}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(save_recipe_url, json=test_recipe_data, headers=headers) as response:
            print(f"\n响应状态码: {response.status}")
            response_text = await response.text()
            print(f"响应内容: {response_text}")
            
            if response.status == 200:
                try:
                    data = json.loads(response_text)
                    print("\n保存成功!")
                    print(f"返回的食谱ID: {data.get('recipe_id')}")
                    print(f"返回的食谱标题: {data.get('title')}")
                    return data
                except json.JSONDecodeError:
                    print("响应不是有效的JSON格式")
                    return None
            else:
                print("保存失败!")
                return None

async def main():
    """
    主测试函数
    """
    print("开始测试保存食谱功能...")
    
    # 1. 登录获取令牌
    token = await login()
    if not token:
        print("登录失败，测试终止")
        return
    
    # 2. 保存食谱
    recipe_data = await save_recipe(token)
    
    if recipe_data:
        print("\n测试成功！保存食谱功能正常工作")
    else:
        print("\n测试失败！保存食谱功能出现问题")

if __name__ == "__main__":
    asyncio.run(main())
