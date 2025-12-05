#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的注册功能
直接测试前端的注册API调用流程
"""

import requests
import json
import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 测试配置
BASE_URL = "http://localhost:8002"
API_ENDPOINT = f"{BASE_URL}/api/auth/register"

# 测试数据 - 使用新的用户名避免冲突
test_data = {
    "username": "testuser_fix_123",
    "email": "testuser_fix_123@example.com",
    "phone": "13100001234",
    "password": "Test@123456"
}

def test_register_api():
    """测试注册API"""
    logger.info("开始测试注册API...")
    logger.info(f"测试数据: {json.dumps(test_data, ensure_ascii=False)}")
    logger.info(f"API端点: {API_ENDPOINT}")
    
    try:
        # 发送注册请求
        response = requests.post(
            API_ENDPOINT,
            json=test_data,
            headers={
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        
        logger.info(f"\n=== 注册响应 ===")
        logger.info(f"状态码: {response.status_code}")
        logger.info(f"响应头: {json.dumps(dict(response.headers), indent=2)}")
        
        try:
            response_data = response.json()
            logger.info(f"响应数据: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        except json.JSONDecodeError:
            logger.info(f"响应文本: {response.text}")
        
        # 检查注册是否成功
        if response.status_code == 200:
            logger.info("\n✅ 注册成功！")
            return True
        else:
            logger.error(f"\n❌ 注册失败，状态码: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"\n❌ 请求异常: {e}")
        return False

def test_login_after_register():
    """测试注册后登录功能"""
    logger.info("\n开始测试注册后登录功能...")
    
    login_data = {
        "username": test_data["username"],
        "password": test_data["password"]
    }
    
    login_endpoint = f"{BASE_URL}/api/auth/login"
    
    try:
        response = requests.post(
            login_endpoint,
            json=login_data,
            headers={
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        
        logger.info(f"\n=== 登录响应 ===")
        logger.info(f"状态码: {response.status_code}")
        
        try:
            response_data = response.json()
            logger.info(f"响应数据: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        except json.JSONDecodeError:
            logger.info(f"响应文本: {response.text}")
        
        if response.status_code == 200:
            logger.info("\n✅ 登录成功！")
            return True
        else:
            logger.error(f"\n❌ 登录失败，状态码: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"\n❌ 请求异常: {e}")
        return False

if __name__ == "__main__":
    logger.info("===========================")
    logger.info("  注册功能修复测试脚本  ")
    logger.info("===========================")
    
    # 测试注册API
    register_success = test_register_api()
    
    # 如果注册成功，测试登录功能
    if register_success:
        login_success = test_login_after_register()
        
        if login_success:
            logger.info("\n🎉 所有测试通过！注册功能修复成功！")
            sys.exit(0)
        else:
            logger.error("\n❌ 登录测试失败！")
            sys.exit(1)
    else:
        logger.error("\n❌ 注册测试失败！")
        sys.exit(1)
