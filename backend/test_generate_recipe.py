#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试食谱生成功能的脚本
"""

import requests
import json
import logging
import os
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("TestRecipeGeneration")

# API基础URL
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/auth/login"
GENERATE_RECIPE_URL = f"{BASE_URL}/ai/generate-recipe"

# 用户凭据（从之前的测试脚本中获取）
USER_CREDENTIALS = {
    "identifier": "徐小昌",
    "password": "Xxc20001018..."
}

def login():
    """
    登录获取访问令牌
    """
    try:
        logger.info("正在登录...")
        response = requests.post(LOGIN_URL, json=USER_CREDENTIALS, headers={"Content-Type": "application/json"})
        logger.info(f"登录响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            logger.info(f"获取到令牌: {token[:20]}...")
            return token
        else:
            logger.error(f"登录失败: {response.text}")
            return None
    except Exception as e:
        logger.error(f"登录过程中发生异常: {str(e)}")
        return None

def test_generate_recipe(token):
    """
    测试生成食谱API
    """
    try:
        logger.info("正在测试生成食谱API...")
        
        # 准备请求头
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # 准备食谱生成请求数据
        recipe_request = {
            "dietary_preferences": ["vegetarian"],
            "food_likes": ["西兰花", "豆腐", "胡萝卜"],
            "food_dislikes": ["洋葱", "大蒜"],
            "health_conditions": [],
            "nutrition_goals": ["low_calorie"],
            "cooking_time_limit": 30,
            "difficulty": "easy",
            "cuisine": "chinese"
        }
        
        logger.info(f"发送食谱生成请求，请求数据: {recipe_request}")
        response = requests.post(GENERATE_RECIPE_URL, headers=headers, json=recipe_request)
        logger.info(f"食谱生成请求状态码: {response.status_code}")
        
        if response.status_code == 200:
            recipe_data = response.json()
            logger.info(f"食谱生成成功，响应数据: {json.dumps(recipe_data, ensure_ascii=False, indent=2)[:500]}...")
            return recipe_data
        else:
            logger.error(f"食谱生成失败: {response.text}")
            return None
    except Exception as e:
        logger.error(f"食谱生成过程中发生异常: {str(e)}", exc_info=True)
        return None

def main():
    """
    主函数
    """
    # 登录获取令牌
    token = login()
    if not token:
        logger.error("无法获取登录令牌，测试失败")
        sys.exit(1)
    
    # 测试生成食谱
    recipe_data = test_generate_recipe(token)
    if recipe_data:
        logger.info("食谱生成测试成功！")
        sys.exit(0)
    else:
        logger.error("食谱生成测试失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()