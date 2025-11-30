#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端到端测试脚本：从用户注册、登录到生成食谱的完整流程
"""

import requests
import json
import time
import uuid

def test_end_to_end_recipe_generation():
    """
    测试从用户注册、登录到生成食谱的完整流程
    """
    print("=== 端到端测试：食谱生成完整流程 ===")
    
    # API端点
    base_url = "http://localhost:8001"
    register_url = f"{base_url}/auth/register"
    login_url = f"{base_url}/auth/login"
    generate_recipe_url = f"{base_url}/ai/generate-recipe"
    
    # 生成随机测试用户
    test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    test_password = "Test123456"
    test_name = "测试用户"
    test_username = f"test_{uuid.uuid4().hex[:8]}"
    
    print(f"\n1. 创建测试用户: {test_email}")
    
    # 1. 注册新用户
    print("\n1.1 注册新用户...")
    register_data = {
        "email": test_email,
        "password": test_password,
        "name": test_name,
        "username": test_username
    }
    
    try:
        register_response = requests.post(register_url, json=register_data)
        print(f"注册状态码: {register_response.status_code}")
        print(f"注册响应: {register_response.text}")
        
        if register_response.status_code == 201:
            print("✅ 用户注册成功")
        else:
            print("❌ 用户注册失败")
            return False
    except Exception as e:
        print(f"❌ 注册请求失败: {e}")
        return False
    
    # 等待用户创建完成
    time.sleep(1)
    
    # 2. 登录获取访问令牌
    print("\n1.2 登录获取访问令牌...")
    login_data = {
        "identifier": test_username,  # 使用username登录
        "password": test_password
    }
    
    try:
        login_response = requests.post(login_url, json=login_data)
        print(f"登录状态码: {login_response.status_code}")
        print(f"登录响应: {login_response.text}")
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            access_token = login_result.get("access_token")
            print(f"✅ 成功获取访问令牌: {access_token[:20]}...")
        else:
            print("❌ 登录失败")
            return False
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return False
    
    # 3. 发送食谱生成请求
    print("\n2. 生成食谱...")
    recipe_data = {
        "dietary_preferences": [],
        "food_likes": ["西红柿", "鸡蛋", "米饭"],
        "food_dislikes": ["香菜"],
        "health_conditions": [],
        "nutrition_goals": [],
        "cooking_time_limit": 20,
        "difficulty": "easy",
        "cuisine": "chinese",
        "ingredients": ["西红柿", "鸡蛋", "米饭"]
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        print("发送食谱生成请求...")
        recipe_response = requests.post(generate_recipe_url, json=recipe_data, headers=headers)
        print(f"食谱生成状态码: {recipe_response.status_code}")
        print(f"食谱生成响应: {recipe_response.text}")
        
        if recipe_response.status_code == 200:
            recipe_result = recipe_response.json()
            print("\n✅ 食谱生成成功！")
            print(f"\n=== 食谱详情 ===")
            print(f"标题: {recipe_result.get('title')}")
            print(f"描述: {recipe_result.get('description')}")
            print(f"烹饪时间: {recipe_result.get('cooking_time')} 分钟")
            print(f"难度: {recipe_result.get('difficulty')}")
            print(f"菜系: {recipe_result.get('cuisine')}")
            
            # 检查是否包含图片URL
            if 'image_url' in recipe_result:
                print(f"\n📷 图片URL: {recipe_result.get('image_url')}")
                print("✅ 食谱包含图片URL！")
                
                # 验证图片URL是否有效
                image_url = recipe_result.get('image_url')
                if image_url.startswith('http'):
                    print("✅ 图片URL格式正确")
                    return True
                else:
                    print("❌ 图片URL格式不正确")
                    return False
            else:
                print("\n❌ 食谱不包含图片URL！")
                print(f"食谱包含的字段: {list(recipe_result.keys())}")
                return False
        else:
            print(f"\n❌ 食谱生成失败，状态码: {recipe_response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ 食谱生成请求失败: {e}")
        import traceback
        print(f"错误详情: {traceback.format_exc()}")
        return False
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    success = test_end_to_end_recipe_generation()
    
    print("\n=== 测试结果摘要 ===")
    if success:
        print("🎉 端到端测试通过！食谱生成流程完整，且包含图片URL")
    else:
        print("❌ 端到端测试失败")
