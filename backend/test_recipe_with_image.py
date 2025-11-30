#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本：验证生成食谱时同时生成AI配图并保存的功能
"""

import requests
import json
import logging
import time

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 测试配置
BASE_URL = "http://localhost:8001"
LOGIN_URL = f"{BASE_URL}/auth/login"
GENERATE_RECIPE_URL = f"{BASE_URL}/ai/generate-recipe"
SAVE_RECIPE_URL = f"{BASE_URL}/ai/save-generated-recipe"

# 测试用户凭据
TEST_USERNAME = "xxiaochang@qq.com"
TEST_PASSWORD = "Xiaochang1234"

def test_login():
    """
    测试用户登录并获取访问令牌
    """
    logger.info(f"尝试登录用户: {TEST_USERNAME}")
    login_data = {
        "identifier": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        logger.info(f"登录请求状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                logger.info("登录成功，获取到访问令牌")
                return token
            else:
                logger.error("登录成功但未获取到访问令牌")
                return None
        else:
            logger.error(f"登录失败: {response.text}")
            return None
    except Exception as e:
        logger.error(f"登录过程中发生异常: {str(e)}")
        return None

def test_generate_recipe_with_image(token):
    """
    测试生成带有图片的食谱
    """
    logger.info("开始测试生成带有图片的食谱")
    
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
    
    try:
        logger.info(f"发送食谱生成请求，请求数据: {recipe_request}")
        response = requests.post(GENERATE_RECIPE_URL, headers=headers, json=recipe_request)
        logger.info(f"食谱生成请求状态码: {response.status_code}")
        
        if response.status_code == 200:
            recipe_data = response.json()
            logger.info(f"食谱生成成功，响应数据: {json.dumps(recipe_data, ensure_ascii=False)[:500]}...")
            
            # 检查是否包含图片URL
            if "image_url" in recipe_data:
                logger.info(f"食谱包含图片URL: {recipe_data['image_url']}")
                return recipe_data
            else:
                logger.error("食谱不包含图片URL")
                return None
        else:
            logger.error(f"食谱生成失败: {response.text}")
            return None
    except Exception as e:
        logger.error(f"食谱生成过程中发生异常: {str(e)}")
        return None

def test_save_recipe_with_image(token, recipe_data):
    """
    测试保存带有图片的食谱
    """
    logger.info("开始测试保存带有图片的食谱")
    
    # 准备请求头
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 准备保存食谱请求数据
    save_request = {
        "recipe_data": recipe_data,
        "share_with_community": False
    }
    
    try:
        logger.info("发送保存食谱请求")
        response = requests.post(SAVE_RECIPE_URL, headers=headers, json=save_request)
        logger.info(f"保存食谱请求状态码: {response.status_code}")
        
        if response.status_code == 200:
            saved_recipe = response.json()
            logger.info(f"食谱保存成功，响应数据: {json.dumps(saved_recipe, ensure_ascii=False)[:500]}...")
            
            # 检查保存的食谱是否包含图片URL
            if "image_url" in saved_recipe:
                logger.info(f"保存的食谱包含图片URL: {saved_recipe['image_url']}")
                return saved_recipe
            else:
                logger.error("保存的食谱不包含图片URL")
                return None
        else:
            logger.error(f"食谱保存失败: {response.text}")
            return None
    except Exception as e:
        logger.error(f"食谱保存过程中发生异常: {str(e)}")
        return None

def main():
    """
    主测试函数
    """
    logger.info("=== 开始测试食谱AI配图生成和保存功能 ===")
    
    # 1. 登录获取令牌
    token = test_login()
    if not token:
        logger.error("登录失败，测试终止")
        return
    
    # 2. 生成带有图片的食谱
    recipe_data = test_generate_recipe_with_image(token)
    if not recipe_data:
        logger.error("生成带有图片的食谱失败，测试终止")
        return
    
    # 3. 保存带有图片的食谱
    saved_recipe = test_save_recipe_with_image(token, recipe_data)
    if not saved_recipe:
        logger.error("保存带有图片的食谱失败，测试终止")
        return
    
    logger.info("=== 所有测试通过！食谱AI配图生成和保存功能正常工作 ===")

if __name__ == "__main__":
    main()
