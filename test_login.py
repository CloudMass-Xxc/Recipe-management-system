import requests
import json

# 测试登录接口
def test_login(identifier, password):
    url = "http://localhost:8002/auth/login"
    headers = {"Content-Type": "application/json"}
    data = {"identifier": identifier, "password": password}
    
    print(f"\nTesting login with identifier: {identifier}")
    print(f"Request URL: {url}")
    print(f"Request headers: {headers}")
    print(f"Request body: {json.dumps(data)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response body: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# 测试手机号登录
test_login("13160697108", "password123")

# 测试邮箱登录
test_login("test@example.com", "password123")

# 测试用户名登录
test_login("testuser123", "password123")
