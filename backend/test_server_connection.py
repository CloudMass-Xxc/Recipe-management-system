#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单的服务器连接测试脚本
"""

import requests
import time

# 测试服务器连接
def test_server_connection():
    """测试服务器连接"""
    url = "http://localhost:8001/health"
    print(f"尝试连接到服务器: {url}")
    
    try:
        response = requests.get(url, timeout=5)
        print(f"连接成功！状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        return True
    except requests.exceptions.ConnectionError as e:
        print(f"连接失败: {e}")
        return False
    except Exception as e:
        print(f"发生异常: {e}")
        return False

# 测试登录API
def test_login_api():
    """测试登录API"""
    url = "http://localhost:8001/auth/login"
    print(f"\n尝试调用登录API: {url}")
    
    # 登录数据
    login_data = {
        "email": "xxiaochang@qq.com",
        "password": "Xiaochang1234"
    }
    
    try:
        response = requests.post(url, json=login_data, timeout=10)
        print(f"登录请求状态码: {response.status_code}")
        print(f"登录响应内容: {response.text}")
        return True
    except requests.exceptions.ConnectionError as e:
        print(f"登录请求连接失败: {e}")
        return False
    except Exception as e:
        print(f"登录请求发生异常: {e}")
        return False

# 主函数
def main():
    """主函数"""
    print("=== 开始测试服务器连接 ===")
    
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)
    
    # 测试服务器连接
    connection_success = test_server_connection()
    
    if connection_success:
        print("\n🎉 服务器连接测试通过！")
        # 测试登录API
        test_login_api()
    else:
        print("\n❌ 服务器连接测试失败！")

if __name__ == "__main__":
    main()