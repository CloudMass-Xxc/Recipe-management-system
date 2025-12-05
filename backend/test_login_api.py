#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试登录功能 - 使用requests库模拟登录请求
"""

import os
import sys
import json
import logging
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('test_login_script')

def test_login(identifier, password="password123"):
    """测试登录功能"""
    try:
        # 构建登录数据
        login_data = {
            "identifier": identifier,
            "password": password
        }
        
        # API URL
        url = "http://localhost:8002/auth/login"
        
        logger.info(f"执行登录测试: {login_data}")
        logger.info(f"API URL: {url}")
        
        # 发送请求
        response = requests.post(
            url,
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        # 输出结果
        logger.info(f"状态码: {response.status_code}")
        logger.info(f"响应内容: {response.text}")
        
        # 分析结果
        if response.status_code == 200:
            try:
                response_data = response.json()
                if "access_token" in response_data:
                    logger.info("✅ 登录成功！获取到访问令牌")
                    logger.info(f"访问令牌: {response_data['access_token'][:20]}...")
                    logger.info(f"用户信息: {response_data.get('user')}")
                    return True
                else:
                    logger.error(f"❌ 登录失败: {response_data}")
                    return False
            except json.JSONDecodeError:
                logger.error(f"❌ 无法解析响应: {response.text}")
                return False
        else:
            logger.error(f"❌ HTTP请求失败: 状态码 {response.status_code}")
            try:
                error_data = response.json()
                logger.error(f"错误详情: {error_data}")
            except json.JSONDecodeError:
                logger.error(f"无法解析错误响应: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"测试登录时发生错误: {e}", exc_info=True)
        return False

def main():
    """主函数"""
    logger.info("开始测试登录功能...")
    
    # 测试1: 使用用户实际的邮箱登录（应该成功）
    logger.info("\n=== 测试1: 使用用户实际的邮箱登录 ===")
    test_login(identifier="xxiaochang@qq.com", password="password123")
    
    # 测试2: 使用用户实际的手机号登录（应该成功）
    logger.info("\n=== 测试2: 使用用户实际的手机号登录 ===")
    test_login(identifier="13160697108", password="password123")
    
    # 测试3: 使用用户实际的用户名登录（应该成功）
    logger.info("\n=== 测试3: 使用用户实际的用户名登录 ===")
    test_login(identifier="xxiaochang", password="password123")
    
    # 测试4: 使用不存在的邮箱登录（应该失败）
    logger.info("\n=== 测试4: 使用不存在的邮箱登录 ===")
    test_login(identifier="nonexistent@example.com", password="password123")
    
    # 测试5: 使用错误的密码登录（应该失败）
    logger.info("\n=== 测试5: 使用错误的密码登录 ===")
    test_login(identifier="xxiaochang@qq.com", password="wrongpassword")
    
    logger.info("\n登录测试完成")

if __name__ == "__main__":
    main()
