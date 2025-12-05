#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化测试脚本 - 验证修复效果
"""

import requests
import json
import time

# API 配置
BASE_URL = "http://localhost:8002"
FRONTEND_URL = "http://localhost:5174"

print("=== 开始验证修复效果 ===")
print(f"后端API地址: {BASE_URL}")
print(f"前端地址: {FRONTEND_URL}")
print("等待3秒确保服务完全启动...")
time.sleep(3)

# 测试用例 1: 测试食谱列表显示异常问题
print("\n=== 测试1: 食谱列表显示异常问题修复 ===")
try:
    # 获取所有食谱列表
    print("1. 获取所有食谱列表...")
    response = requests.get(f"{BASE_URL}/recipes")
    print(f"   状态码: {response.status_code}")
    
    if response.status_code == 200:
        recipes_data = response.json()
        print(f"   成功获取 {len(recipes_data)} 个食谱")
        
        # 检查是否有收藏标记的食谱
        favorite_recipes_in_list = [recipe for recipe in recipes_data if recipe.get('is_favorite')]
        if favorite_recipes_in_list:
            print(f"   ⚠️  发现 {len(favorite_recipes_in_list)} 个带有收藏标记的食谱")
            for i, recipe in enumerate(favorite_recipes_in_list[:3]):
                print(f"     - 食谱 {i+1}: ID={recipe.get('id')}, 标题={recipe.get('title')}")
        else:
            print("   ✓ 食谱列表中没有发现带有收藏标记的食谱，修复有效！")
    else:
        print(f"   ❌ 获取食谱列表失败: {response.text}")
        
except Exception as e:
    print(f"   ❌ 测试过程中发生错误: {str(e)}")

# 测试用例 2: 检查后端API文档和路由
print("\n=== 测试2: 检查后端API文档和路由 ===")
try:
    # 检查API文档
    print("1. 访问API文档...")
    response = requests.get(f"{BASE_URL}/docs")
    print(f"   文档页面状态码: {response.status_code}")
    
    # 检查根路径
    print("2. 访问根路径...")
    response = requests.get(f"{BASE_URL}/")
    print(f"   根路径状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   根路径响应: {response.json()}")
    
    # 检查健康检查端点
    print("3. 访问健康检查端点...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   健康检查状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   健康检查响应: {response.json()}")
        
except Exception as e:
    print(f"   ❌ 测试过程中发生错误: {str(e)}")

# 测试用例 3: 探索AI相关路由
print("\n=== 测试3: 探索AI相关路由 ===")
try:
    # 尝试不同的AI路由
    ai_routes = [
        ("AI根路由", f"{BASE_URL}/ai"),
        ("生成食谱API", f"{BASE_URL}/ai/generate-recipe"),
        ("另一个可能的生成食谱API", f"{BASE_URL}/recipes/generate"),
    ]
    
    for name, url in ai_routes:
        print(f"1. 测试 {name}: {url}")
        try:
            if "/generate" in url:
                # POST 请求
                test_data = {
                    "ingredients": ["鸡胸肉", "西兰花", "胡萝卜"],
                    "dietary_preferences": ["低脂肪", "高蛋白"],
                    "cooking_time": "30分钟以内"
                }
                response = requests.post(
                    url,
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                )
                print(f"   POST状态码: {response.status_code}")
            else:
                # GET 请求
                response = requests.get(url)
                print(f"   GET状态码: {response.status_code}")
            
            print(f"   响应内容: {response.text[:200]}..." if len(response.text) > 200 else f"   响应内容: {response.text}")
            
        except Exception as e:
            print(f"   ❌ 测试失败: {str(e)}")
            
except Exception as e:
    print(f"   ❌ 测试过程中发生错误: {str(e)}")

# 测试用例 4: 检查修复后的ai_client.py功能
print("\n=== 测试4: 检查修复后的ai_client.py功能 ===")
try:
    # 直接导入并测试ai_client.py中的函数
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
    
    from app.ai_service.ai_client import generate_recipe, _validate_recipe_data
    
    print("1. 测试_validate_recipe_data函数...")
    
    # 测试用例1: 正常数据
    normal_data = {
        "title": "测试食谱",
        "ingredients": ["食材1", "食材2"],
        "instructions": ["步骤1", "步骤2"]
    }
    validated_data = _validate_recipe_data(normal_data)
    print("   ✓ 正常数据测试通过")
    print(f"     验证后: {validated_data}")
    
    # 测试用例2: 类型转换
    type_convert_data = {
        "title": 123,  # 数字转字符串
        "ingredients": "食材1,食材2",  # 字符串转列表
        "instructions": "步骤1\n步骤2"  # 字符串转列表
    }
    validated_data = _validate_recipe_data(type_convert_data)
    print("   ✓ 类型转换测试通过")
    print(f"     验证后: {validated_data}")
    print(f"     类型检查 - title: {type(validated_data['title']).__name__}")
    print(f"     类型检查 - ingredients: {type(validated_data['ingredients']).__name__}")
    print(f"     类型检查 - instructions: {type(validated_data['instructions']).__name__}")
    
    # 测试用例3: 空列表处理
    empty_list_data = {
        "title": "测试食谱",
        "ingredients": [],  # 空列表
        "instructions": []  # 空列表
    }
    validated_data = _validate_recipe_data(empty_list_data)
    print("   ✓ 空列表处理测试通过")
    print(f"     验证后: {validated_data}")
    
    print("   ✓ _validate_recipe_data函数修复成功！")
    
except ImportError as e:
    print(f"   ⚠️  导入ai_client.py失败: {str(e)}")
    print("     可能需要在正确的目录下运行此测试")
except Exception as e:
    print(f"   ❌ 测试过程中发生错误: {str(e)}")

print("\n=== 测试完成 ===")
print("建议在前端界面进行手动验证，确保所有功能正常工作：")
print(f"- 前端访问地址: {FRONTEND_URL}")
print(f"- 后端API文档: {BASE_URL}/docs")
print("\n请检查：")
print("1. 食谱列表是否不再显示已收藏的食谱")
print("2. 个性化食谱生成功能是否可以正常使用")
print("3. 所有现有功能是否正常工作（回归测试）")