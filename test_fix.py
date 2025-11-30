import requests
import json
import time

# 测试函数
def test_endpoint(url, method, headers=None, json_data=None, expected_status_code=None):
    print(f"\nTesting {method} {url}")
    print(f"Headers: {headers}")
    print(f"Body: {json.dumps(json_data, ensure_ascii=False, indent=2) if json_data else None}")
    
    try:
        if method == "POST":
            response = requests.post(url, headers=headers, json=json_data)
        elif method == "GET":
            response = requests.get(url, headers=headers)
        else:
            print(f"Unsupported method: {method}")
            return None
        
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        try:
            response_data = response.json()
            print(f"Response body: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        except json.JSONDecodeError:
            print(f"Response body (not JSON): {response.text}")
            response_data = None
        
        if expected_status_code and response.status_code != expected_status_code:
            print(f"❌ Expected status code {expected_status_code}, got {response.status_code}")
        else:
            print(f"✅ Status code {'matches expected' if expected_status_code else 'received'}")
        
        return response
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

# 配置
base_url = "http://localhost:8002"
headers = {"Content-Type": "application/json"}

# 测试用户数据
new_user = {
    "username": "testuser_new",
    "email": "test_new@example.com",
    "phone": "13800138000",
    "password": "password123"
}

# 1. 测试注册新用户（使用手机号）
print("\n" + "="*50)
print("1. Testing user registration with phone number")
print("="*50)
register_response = test_endpoint(
    f"{base_url}/auth/register",
    "POST",
    headers=headers,
    json_data=new_user,
    expected_status_code=201
)

# 等待一点时间，确保数据已保存
time.sleep(1)

# 2. 测试使用手机号登录
print("\n" + "="*50)
print("2. Testing login with phone number")
print("="*50)
phone_login_response = test_endpoint(
    f"{base_url}/auth/login",
    "POST",
    headers=headers,
    json_data={"identifier": new_user["phone"], "password": new_user["password"]},
    expected_status_code=200
)

# 3. 测试使用邮箱登录
print("\n" + "="*50)
print("3. Testing login with email")
print("="*50)
email_login_response = test_endpoint(
    f"{base_url}/auth/login",
    "POST",
    headers=headers,
    json_data={"identifier": new_user["email"], "password": new_user["password"]},
    expected_status_code=200
)

# 4. 测试使用用户名登录
print("\n" + "="*50)
print("4. Testing login with username")
print("="*50)
username_login_response = test_endpoint(
    f"{base_url}/auth/login",
    "POST",
    headers=headers,
    json_data={"identifier": new_user["username"], "password": new_user["password"]},
    expected_status_code=200
)

# 总结测试结果
print("\n" + "="*50)
print("TEST SUMMARY")
print("="*50)
print(f"Registration: {'SUCCESS' if register_response and register_response.status_code == 201 else 'FAILED'}")
print(f"Login with phone: {'SUCCESS' if phone_login_response and phone_login_response.status_code == 200 else 'FAILED'}")
print(f"Login with email: {'SUCCESS' if email_login_response and email_login_response.status_code == 200 else 'FAILED'}")
print(f"Login with username: {'SUCCESS' if username_login_response and username_login_response.status_code == 200 else 'FAILED'}")
