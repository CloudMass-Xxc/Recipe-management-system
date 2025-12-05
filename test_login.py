import requests
import json

# 测试登录API
def test_login():
    url = "http://localhost:8002/api/auth/login"
    headers = {"Content-Type": "application/json"}
    data = {
        "username": "testuser_d6be1c2988bbe5cd",
        "password": "Test@1234"
    }
    
    print(f"发送登录请求到: {url}")
    print(f"请求头: {headers}")
    print(f"请求体: {json.dumps(data)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应体: {response.text}")
        
        if response.status_code == 200:
            print("\n登录成功!")
        else:
            print(f"\n登录失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"\n请求失败: {str(e)}")

# 测试获取当前用户信息
def test_me(token):
    url = "http://localhost:8002/api/auth/me"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    print(f"\n发送获取用户信息请求到: {url}")
    print(f"请求头: {headers}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应体: {response.text}")
        
        if response.status_code == 200:
            print("\n获取用户信息成功!")
        else:
            print(f"\n获取用户信息失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"\n请求失败: {str(e)}")

if __name__ == "__main__":
    test_login()