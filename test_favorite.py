#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json

# 登录请求
def login():
    url = "http://localhost:8002/api/auth/login"
    headers = {"Content-Type": "application/json"}
    data = {"username": "testuser2", "password": "Test123!"}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 如果响应状态码不是200，抛出异常
        
        print(f"登录成功，状态码: {response.status_code}")
        
        # 尝试解析响应内容
        try:
            json_response = response.json()
            print("响应内容:")
            print(json.dumps(json_response, indent=2, ensure_ascii=False))
            
            # 检查是否有访问令牌
            if "data" in json_response and "access_token" in json_response["data"]:
                print(f"\n访问令牌: {json_response['data']['access_token']}")
                return json_response['data']['access_token']
            else:
                print("\n响应中没有访问令牌")
                return None
                
        except json.JSONDecodeError as e:
            print(f"解析JSON响应失败: {e}")
            print(f"原始响应内容: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"登录请求失败: {e}")
        return None

# 测试收藏功能
def test_favorite(access_token, recipe_id):
    if not access_token:
        print("没有访问令牌，无法测试收藏功能")
        return
    
    url = f"http://localhost:8002/api/recipes/{recipe_id}/favorite"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.post(url, headers=headers, json={})
        
        print(f"\n收藏食谱请求，状态码: {response.status_code}")
        
        try:
            json_response = response.json()
            print("响应内容:")
            print(json.dumps(json_response, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(f"原始响应内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"收藏请求失败: {e}")

if __name__ == "__main__":
    # 测试登录
    token = login()
    
    # 测试收藏功能（使用一个示例食谱ID）
    if token:
        test_recipe_id = "583d7d70-b89c-494b-8d66-0e60f8484428"
        test_favorite(token, test_recipe_id)
