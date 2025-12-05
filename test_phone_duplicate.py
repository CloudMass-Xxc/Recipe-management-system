#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手机号重复检测功能测试脚本
"""

import json
import logging
import requests
import random
import time
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 测试配置
API_URL = "http://localhost:8002/api/auth/register"


def generate_random_phone():
    """生成随机手机号码"""
    prefixes = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                "150", "151", "152", "153", "155", "156", "157", "158", "159",
                "170", "171", "172", "173", "175", "176", "177", "178",
                "180", "181", "182", "183", "184", "185", "186", "187", "188", "189"]
    
    prefix = random.choice(prefixes)
    suffix = ''.join(random.choices('0123456789', k=8))
    
    return prefix + suffix


def test_phone_duplicate_detection():
    """测试手机号重复检测功能"""
    logger.info("=" * 30)
    logger.info("    手机号重复检测测试    ")
    logger.info("=" * 30)
    
    # 生成唯一的测试数据
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_phone = generate_random_phone()
    
    # 测试1: 先注册一个用户
    logger.info("\n测试1: 注册第一个用户（使用新手机号）")
    user1_data = {
        "username": f"user1_{timestamp}",
        "email": f"user1_{timestamp}@example.com",
        "phone": test_phone,
        "password": "Test@123456"
    }
    
    logger.info(f"用户1数据: {json.dumps(user1_data, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            API_URL,
            json=user1_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        logger.info(f"\n用户1注册响应: 状态码={response.status_code}")
        
        try:
            response_data = response.json()
            logger.info(f"响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        except json.JSONDecodeError:
            logger.info(f"响应内容: {response.text}")
        
        if (response.status_code in [200, 201] and 
            response_data and 
            response_data.get("success") == True):
            logger.info("✅ 测试1通过: 第一个用户注册成功")
        else:
            logger.error("❌ 测试1失败: 第一个用户注册失败")
            return False
            
    except Exception as e:
        logger.error(f"❌ 测试1失败: 发生异常 - {str(e)}")
        return False
    
    # 测试2: 尝试用不同的用户名和邮箱，但相同的手机号注册
    logger.info("\n测试2: 尝试用相同手机号注册第二个用户")
    user2_data = {
        "username": f"user2_{timestamp}",
        "email": f"user2_{timestamp}@example.com",
        "phone": test_phone,  # 使用与用户1相同的手机号
        "password": "Test@123456"
    }
    
    logger.info(f"用户2数据: {json.dumps(user2_data, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            API_URL,
            json=user2_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        logger.info(f"\n用户2注册响应: 状态码={response.status_code}")
        
        try:
            response_data = response.json()
            logger.info(f"响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        except json.JSONDecodeError:
            logger.info(f"响应内容: {response.text}")
        
        # 期望的行为：返回400状态码和"手机号已被注册"的错误信息
        if (response.status_code == 400 and 
            response_data and 
            response_data.get("error") and 
            "手机号已被注册" in response_data["error"].get("message", "")):
            logger.info("✅ 测试2通过: 正确检测到手机号重复")
            logger.info("✅ 手机号重复检测功能正常工作！")
        else:
            logger.error("❌ 测试2失败: 没有正确检测到手机号重复")
            logger.error(f"期望: 400状态码 + '手机号已被注册'错误")
            logger.error(f"实际: {response.status_code}状态码 + {response_data}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 测试2失败: 发生异常 - {str(e)}")
        return False
    
    logger.info("\n" + "=" * 30)
    logger.info("✅ 所有测试通过！")
    logger.info("✅ 手机号重复检测功能正常！")
    logger.info("=" * 30)
    
    return True


if __name__ == "__main__":
    success = test_phone_duplicate_detection()
    exit(0 if success else 1)
