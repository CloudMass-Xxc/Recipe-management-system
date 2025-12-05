#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试用户注册和登录功能的脚本
"""

import requests
import logging
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('test_auth')

# API端点
BASE_URL = "http://localhost:8000/api"
REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login"

# 测试用户数据
TEST_USER = {
    "username": "testuser2",
    "email": "test2@example.com",
    "phone": "13900139000",
    "password": "Test123!"
}

def test_register():
    """测试用户注册功能"""
    logger.info("=== 开始测试用户注册功能 ===")
    logger.info(f"注册URL: {REGISTER_URL}")
    logger.info(f"注册数据: {TEST_USER}")
    
    try:
        # 发送注册请求
        response = requests.post(REGISTER_URL, json=TEST_USER)
        logger.info(f"注册响应状态码: {response.status_code}")
        logger.info(f"注册响应内容: {response.text}")
        
        if response.status_code == 200:
            logger.info("✅ 用户注册成功")
            return True
        else:
            logger.error(f"❌ 用户注册失败: {response.status_code}")
            logger.error(f"错误信息: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ 注册请求异常: {str(e)}")
        return False

def test_login():
    """测试用户登录功能"""
    logger.info("=== 开始测试用户登录功能 ===")
    logger.info(f"登录URL: {LOGIN_URL}")
    
    # 准备登录数据
    login_data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    }
    logger.info(f"登录数据: {login_data}")
    
    try:
        # 发送登录请求
        response = requests.post(LOGIN_URL, json=login_data)
        logger.info(f"登录响应状态码: {response.status_code}")
        logger.info(f"登录响应内容: {response.text}")
        
        if response.status_code == 200:
            logger.info("✅ 用户登录成功")
            return response.json()
        else:
            logger.error(f"❌ 用户登录失败: {response.status_code}")
            logger.error(f"错误信息: {response.text}")
            return None
    except Exception as e:
        logger.error(f"❌ 登录请求异常: {str(e)}")
        return None

def test_email_login():
    """测试使用邮箱登录功能"""
    logger.info("=== 开始测试使用邮箱登录功能 ===")
    logger.info(f"登录URL: {LOGIN_URL}")
    
    # 准备登录数据（使用邮箱）
    login_data = {
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    logger.info(f"登录数据: {login_data}")
    
    try:
        # 发送登录请求
        response = requests.post(LOGIN_URL, json=login_data)
        logger.info(f"登录响应状态码: {response.status_code}")
        logger.info(f"登录响应内容: {response.text}")
        
        if response.status_code == 200:
            logger.info("✅ 使用邮箱登录成功")
            return response.json()
        else:
            logger.error(f"❌ 使用邮箱登录失败: {response.status_code}")
            logger.error(f"错误信息: {response.text}")
            return None
    except Exception as e:
        logger.error(f"❌ 登录请求异常: {str(e)}")
        return None

def test_phone_login():
    """测试使用手机号登录功能"""
    logger.info("=== 开始测试使用手机号登录功能 ===")
    logger.info(f"登录URL: {LOGIN_URL}")
    
    # 准备登录数据（使用手机号）
    login_data = {
        "username": TEST_USER["phone"],
        "password": TEST_USER["password"]
    }
    logger.info(f"登录数据: {login_data}")
    
    try:
        # 发送登录请求
        response = requests.post(LOGIN_URL, json=login_data)
        logger.info(f"登录响应状态码: {response.status_code}")
        logger.info(f"登录响应内容: {response.text}")
        
        if response.status_code == 200:
            logger.info("✅ 使用手机号登录成功")
            return response.json()
        else:
            logger.error(f"❌ 使用手机号登录失败: {response.status_code}")
            logger.error(f"错误信息: {response.text}")
            return None
    except Exception as e:
        logger.error(f"❌ 登录请求异常: {str(e)}")
        return None

if __name__ == "__main__":
    logger.info("开始测试认证功能...")
    
    # 测试注册
    if test_register():
        # 测试使用用户名登录
        login_result = test_login()
        
        if login_result:
            # 测试使用邮箱登录
            test_email_login()
            
            # 测试使用手机号登录
            test_phone_login()
    
    logger.info("认证功能测试完成")
