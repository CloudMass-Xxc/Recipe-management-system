#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试个人资料API端点
验证 /users/me GET 和 PUT 方法是否正常工作
"""

import requests
import json
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('test_profile_api')

# API配置
BASE_URL = "http://localhost:8002"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
PROFILE_URL = f"{BASE_URL}/api/users/me"

# 测试用户凭据
TEST_USER = {
    "username": "testuser2",  # 更新为刚刚测试成功的用户名
    "password": "Test123!"
}

def test_login():
    """测试登录功能，获取访问令牌"""
    logger.info("开始测试登录功能...")
    logger.info(f"登录URL: {LOGIN_URL}")
    logger.info(f"用户名: {TEST_USER['username']}")
    
    try:
        response = requests.post(
            LOGIN_URL,
            headers={"Content-Type": "application/json"},
            json=TEST_USER
        )
        
        logger.info(f"登录响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            # 从响应的data字段中获取access_token
            access_token = data.get('data', {}).get('access_token')
            if access_token:
                logger.info(f"✅ 登录成功！获取到访问令牌")
                return access_token
            else:
                logger.error("❌ 登录成功，但未获取到访问令牌")
                logger.error(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
                return None
        else:
            logger.error(f"❌ 登录失败: {response.status_code}")
            try:
                error_data = response.json()
                logger.error(f"错误信息: {json.dumps(error_data, ensure_ascii=False, indent=2)}")
            except:
                logger.error(f"响应内容: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"❌ 登录请求异常: {str(e)}")
        return None

def test_get_profile(access_token):
    """测试获取个人资料功能"""
    logger.info("\n开始测试获取个人资料功能...")
    logger.info(f"个人资料URL: {PROFILE_URL}")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(PROFILE_URL, headers=headers)
        
        logger.info(f"获取个人资料响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ 获取个人资料成功！")
            logger.info(f"个人资料数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            return data
        else:
            logger.error(f"❌ 获取个人资料失败: {response.status_code}")
            try:
                error_data = response.json()
                logger.error(f"错误信息: {json.dumps(error_data, ensure_ascii=False, indent=2)}")
            except:
                logger.error(f"响应内容: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"❌ 获取个人资料请求异常: {str(e)}")
        return None

def test_update_profile(access_token, profile_data):
    """测试更新个人资料功能"""
    logger.info("\n开始测试更新个人资料功能...")
    logger.info(f"个人资料URL: {PROFILE_URL}")
    
    # 准备更新数据
    update_data = {
        "display_name": "测试用户更新",
        "bio": "这是一个更新后的个人简介",
        "diet_preferences": ["vegetarian", "low_carb"]
    }
    
    logger.info(f"更新数据: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.put(PROFILE_URL, headers=headers, json=update_data)
        
        logger.info(f"更新个人资料响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ 更新个人资料成功！")
            logger.info(f"更新后的个人资料: {json.dumps(data, ensure_ascii=False, indent=2)}")
            return data
        else:
            logger.error(f"❌ 更新个人资料失败: {response.status_code}")
            try:
                error_data = response.json()
                logger.error(f"错误信息: {json.dumps(error_data, ensure_ascii=False, indent=2)}")
            except:
                logger.error(f"响应内容: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"❌ 更新个人资料请求异常: {str(e)}")
        return None

def test_profile_api():
    """测试完整的个人资料API功能"""
    logger.info("===== 开始测试个人资料API =====")
    
    # 1. 登录获取令牌
    access_token = test_login()
    if not access_token:
        logger.error("登录失败，无法继续测试")
        return False
    
    # 2. 获取个人资料
    profile_data = test_get_profile(access_token)
    if not profile_data:
        logger.error("获取个人资料失败，无法继续测试")
        return False
    
    # 3. 更新个人资料
    updated_profile = test_update_profile(access_token, profile_data)
    if not updated_profile:
        logger.error("更新个人资料失败")
        return False
    
    # 4. 再次获取个人资料，验证更新是否成功
    final_profile = test_get_profile(access_token)
    if not final_profile:
        logger.error("验证更新后个人资料失败")
        return False
    
    # 验证更新是否生效
    if (final_profile.get('display_name') == "测试用户更新" and
        final_profile.get('bio') == "这是一个更新后的个人简介" and
        final_profile.get('diet_preferences') == ["vegetarian", "low_carb"]):
        logger.info("\n✅ 个人资料更新验证成功！所有字段都已正确更新")
        logger.info("===== 个人资料API测试全部通过！=====")
        return True
    else:
        logger.error("\n❌ 个人资料更新验证失败！某些字段未正确更新")
        logger.error(f"期望的display_name: 测试用户更新, 实际: {final_profile.get('display_name')}")
        logger.error(f"期望的bio: 这是一个更新后的个人简介, 实际: {final_profile.get('bio')}")
        logger.error(f"期望的diet_preferences: ['vegetarian', 'low_carb'], 实际: {final_profile.get('diet_preferences')}")
        logger.error("===== 个人资料API测试失败！=====")
        return False

if __name__ == "__main__":
    test_profile_api()
