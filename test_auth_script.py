#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试认证功能的脚本
"""
import requests
import json
import sys

def test_login():
    """测试登录功能"""
    base_url = "http://localhost:8002"
    login_endpoint = f"{base_url}/auth/login"
    
    test_user = {
        "username": "testuser123",
        "email": "test@example.com",
        "phone": "13160697108",
        "password": "password123"
    }
    
    print("=" * 60)
    print("🔍 测试登录功能")
    print("=" * 60)
    
    # 测试不同的登录标识符格式
    identifier_types = [
        ("手机号", test_user["phone"]),
        ("邮箱", test_user["email"]),
        ("用户名", test_user["username"])
    ]
    
    for identifier_type, identifier in identifier_types:
        print(f"\n测试使用{identifier_type}登录: {identifier}")
        print("-" * 30)
        try:
            login_data = {
                "identifier": identifier,
                "password": test_user["password"]
            }
            
            print(f"发送登录请求到: {login_endpoint}")
            print(f"请求数据: {json.dumps(login_data, ensure_ascii=False)}")
            
            response = requests.post(
                login_endpoint,
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"\n响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                print(f"✅ 使用{identifier_type}登录成功！")
                return True
            else:
                print(f"❌ 使用{identifier_type}登录失败！")
                
        except Exception as e:
            print(f"❌ 登录时发生错误: {e}")
    
    return False

if __name__ == "__main__":
    success = test_login()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    success = test_auth()
    sys.exit(0 if success else 1)
