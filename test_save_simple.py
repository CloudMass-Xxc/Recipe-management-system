#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本：直接测试保存食谱API
使用固定的测试用户ID，绕过登录步骤
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"
TEST_USER_ID = "test_user_id"  # 测试用户ID

# 读取测试数据
with open("test_recipe_data.json", "r", encoding="utf-8") as f:
    recipe_data = json.load(f)

print("===== 简单测试保存食谱API =====")
print(f"测试API端点: {BASE_URL}/ai/save-generated-recipe")
print(f"使用测试用户ID: {TEST_USER_ID}")

# 修改数据以使用测试用户ID
recipe_data["recipe_data"]["author_id"] = TEST_USER_ID

print("\n请求体数据结构:")
print(f"- 食谱标题: {recipe_data['recipe_data'].get('title')}")
print(f"- 食谱描述: {recipe_data['recipe_data'].get('description')}")
print(f"- 食材数量: {len(recipe_data['recipe_data'].get('ingredients', []))}")
print(f"- 烹饪步骤类型: {type(recipe_data['recipe_data'].get('instructions'))}")
print(f"- 烹饪步骤内容(前100字符): {recipe_data['recipe_data'].get('instructions')[:100]}...")
print(f"- 标签: {recipe_data['recipe_data'].get('tags')}")
print(f"- 营养信息: {recipe_data['recipe_data'].get('nutrition_info')}")

# 测试API调用（使用测试令牌，实际认证会被测试代码绕过）
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer test_token"
}

try:
    print("\n🚀 正在调用保存食谱API...")
    response = requests.post(
        f"{BASE_URL}/ai/save-generated-recipe",
        json=recipe_data,
        headers=headers,
        timeout=30
    )
    
    print(f"\n📊 API响应:")
    print(f"- 状态码: {response.status_code}")
    print(f"- 响应内容: {response.text}")
    
    if response.status_code == 200:
        print("\n🎉 API调用成功！")
    else:
        print(f"\n❌ API调用失败，状态码: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"\n💥 API调用异常: {str(e)}")

print("\n===== 测试完成 =====")
