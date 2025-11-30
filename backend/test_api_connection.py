#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试API连接脚本
"""

import requests
import sys

def test_api_connection():
    """测试API连接"""
    print("=== 测试API连接 ===")
    
    # 测试健康检查端点
    health_url = "http://127.0.0.1:8000/health"
    print(f"测试健康检查端点: {health_url}")
    
    try:
        response = requests.get(health_url, timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
        print("✅ 健康检查端点测试通过")
    except Exception as e:
        print(f"❌ 健康检查端点测试失败: {str(e)}")
        return False
    
    # 测试根路径
    root_url = "http://127.0.0.1:8000/"
    print(f"\n测试根路径: {root_url}")
    
    try:
        response = requests.get(root_url, timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
        print("✅ 根路径测试通过")
    except Exception as e:
        print(f"❌ 根路径测试失败: {str(e)}")
        return False
    
    print("\n🎉 所有API连接测试都通过了！")
    return True

if __name__ == "__main__":
    success = test_api_connection()
    sys.exit(0 if success else 1)
