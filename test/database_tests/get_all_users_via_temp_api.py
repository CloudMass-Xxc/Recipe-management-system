#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通过临时API获取所有用户信息的脚本
利用临时添加的/auth/users-list端点获取所有用户数据
"""

import os
import sys
import json
import requests

# 后端服务基础URL
BASE_URL = "http://localhost:8000"

class TempUserInfoFetcher:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {"Content-Type": "application/json"}
    
    def fetch_all_users(self):
        """
        调用临时端点获取所有用户信息
        """
        print("\n尝试通过临时端点获取所有用户信息...")
        print(f"请求URL: {self.base_url}/auth/users-list")
        
        try:
            # 直接调用临时端点，不需要登录
            response = requests.get(
                f"{self.base_url}/auth/users-list",
                headers=self.headers
            )
            
            if response.status_code == 200:
                users = response.json()
                print(f"✅ 获取成功！发现 {len(users)} 个用户")
                return users
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
        
        print("\n" + "=" * 80)
        print(f"{'用户信息列表':^78}")
        print("=" * 80)
        
        # 打印表头
        print(f"{'用户ID':^36} | {'用户名':^15} | {'邮箱':^20}")
        print("-" * 80)
        
        for user in users:
            # 格式化输出，确保对齐
            user_id = user.get('user_id', 'N/A')
            username = user.get('username', 'N/A')
            email = user.get('email', 'N/A')
            
            print(f"{user_id[:32]:<36} | {username:<15} | {email:<20}")
        
        print("\n" + "=" * 80)
        print(f"总计: {len(users)} 个用户")
        print("=" * 80)
        
        # 显示详细信息
        print("\n详细信息:")
        for idx, user in enumerate(users, 1):
            print(f"\n用户 {idx}:")
            print(f"  - 用户ID: {user.get('user_id', 'N/A')}")
            print(f"  - 用户名: {user.get('username', 'N/A')}")
            print(f"  - 邮箱: {user.get('email', 'N/A')}")
            print(f"  - 手机号: {user.get('phone', 'N/A')}")
            print(f"  - 显示名称: {user.get('display_name', 'N/A')}")
            print(f"  - 创建时间: {user.get('created_at', 'N/A')}")
    
    def run(self):
        """
        运行主流程
        """
        print("\n" + "=" * 60)
        print(f"{'通过临时API获取所有用户信息':^58}")
        print("=" * 60)
        print("注意: 此脚本使用临时添加的API端点，仅用于调试")
        
        # 获取所有用户
        users = self.fetch_all_users()
        
        if users:
            # 显示用户信息
            self.display_users_info(users)
        else:
            print("\n❌ 无法获取用户列表，请检查后端服务是否正常运行")
        
        print("\n程序执行完毕")

if __name__ == "__main__":
    fetcher = TempUserInfoFetcher()
    fetcher.run()