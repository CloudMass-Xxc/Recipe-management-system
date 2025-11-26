#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通过API获取所有用户信息的脚本
利用管理员专用的/users接口来获取所有用户数据
"""

import os
import sys
import json
import requests

# 后端服务基础URL
BASE_URL = "http://localhost:8000"

class UserInfoFetcher:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {"Content-Type": "application/json"}
    
    def login_as_test_user(self):
        """
        使用测试账号登录获取token
        """
        print("\n[1] 尝试使用测试账号登录...")
        
        login_data = {
            "phone": "13160697108",
            "password": "password123"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json=login_data,
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                if token:
                    print(f"✅ 登录成功，获取到token")
                    # 更新headers，添加Authorization
                    self.headers["Authorization"] = f"Bearer {token}"
                    return True
                else:
                    print(f"❌ 登录响应中没有token")
                    print(f"响应内容: {data}")
            else:
                print(f"❌ 登录失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
        except Exception as e:
            print(f"❌ 登录请求异常: {str(e)}")
        
        return False
    
    def get_all_users(self):
        """
        尝试获取所有用户信息
        """
        print("\n[2] 尝试获取所有用户信息...")
        
        try:
            response = requests.get(
                f"{self.base_url}/users",
                headers=self.headers
            )
            
            if response.status_code == 200:
                users = response.json()
                print(f"✅ 获取成功！发现 {len(users)} 个用户")
                return users
            elif response.status_code == 403:
                print(f"❌ 权限不足 (403 Forbidden)")
                print(f"这个接口需要管理员权限")
                print(f"响应内容: {response.text}")
                return None
            else:
                print(f"❌ 获取失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None
        except Exception as e:
            print(f"❌ 请求异常: {str(e)}")
            return None
    
    def display_users_info(self, users):
        """
        显示用户信息
        """
        if not users:
            print("没有用户数据可显示")
            return
        
        print("\n" + "=" * 60)
        print(f"{'用户信息列表':^58}")
        print("=" * 60)
        
        for idx, user in enumerate(users, 1):
            print(f"\n用户 {idx}:")
            print(f"- 用户ID: {user.get('user_id', 'N/A')}")
            print(f"- 用户名: {user.get('username', 'N/A')}")
            print(f"- 邮箱: {user.get('email', 'N/A')}")
            print(f"- 手机号: {user.get('phone', 'N/A')}")
            print(f"- 显示名称: {user.get('display_name', 'N/A')}")
            print(f"- 创建时间: {user.get('created_at', 'N/A')}")
            print("-" * 40)
        
        print("\n" + "=" * 60)
        print(f"总计: {len(users)} 个用户")
        print("=" * 60)
    
    def run(self):
        """
        运行主流程
        """
        print("\n" + "=" * 50)
        print(f"{'通过API获取用户列表':^48}")
        print("=" * 50)
        
        # 1. 登录获取token
        if not self.login_as_test_user():
            print("\n❌ 无法获取访问权限，程序退出")
            return
        
        # 2. 获取所有用户
        users = self.get_all_users()
        
        if users:
            # 3. 显示用户信息
            self.display_users_info(users)
        else:
            print("\n💡 提示：需要管理员权限才能获取所有用户列表")
            print("   请联系系统管理员或尝试其他方法")
        
        print("\n程序执行完毕")

if __name__ == "__main__":
    fetcher = UserInfoFetcher()
    fetcher.run()