import requests
import json

# 测试API路径的脚本
def test_register_api():
    # 测试正确的API路径
    correct_url = 'http://localhost:8002/api/auth/register'
    # 测试错误的API路径
    wrong_url = 'http://localhost:8002/auth/register'
    
    # 测试数据
    test_data = {
        "username": "test_user_api",
        "email": "test_api@example.com",
        "phone": "13800138000",
        "password": "Test123456!"
    }
    
    print("测试API路径:")
    print(f"正确路径: {correct_url}")
    print(f"错误路径: {wrong_url}")
    print("测试数据:", json.dumps(test_data, ensure_ascii=False))
    print("\n===== 测试开始 =====")
    
    # 测试错误路径
    print("\n1. 测试错误路径 (/auth/register):")
    try:
        response = requests.post(wrong_url, json=test_data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试正确路径
    print("\n2. 测试正确路径 (/api/auth/register):")
    try:
        response = requests.post(correct_url, json=test_data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试登录API
    print("\n3. 测试登录API (/api/auth/login):")
    try:
        login_data = {
            "identifier": "test_user_api",
            "password": "Test123456!"
        }
        response = requests.post('http://localhost:8002/api/auth/login', json=login_data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    test_register_api()
