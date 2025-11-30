import requests
import json

# 使用之前成功注册的用户信息（从测试输出中获取）
test_user = {
    "username": "testuser_f4dfd834",
    "email": "test_f4dfd834@example.com",
    "phone": "13f4dfd834",  # 这个手机号包含字母字符
    "password": "password123"
}

# 测试登录功能
def test_login(identifier, password, identifier_type):
    url = "http://localhost:8002/auth/login"
    headers = {"Content-Type": "application/json"}
    login_data = {"identifier": identifier, "password": password}
    
    print(f"\n=== Testing Login with {identifier_type} ===")
    print(f"URL: {url}")
    print(f"Login Data: {json.dumps(login_data, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, headers=headers, json=login_data)
        print(f"Response Status Code: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"Response Body: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        except json.JSONDecodeError:
            print(f"Response Body (not JSON): {response.text}")
            
        if response.status_code == 200:
            print("✅ Login Successful!")
        else:
            print("❌ Login Failed")
            
    except requests.exceptions.RequestException as e:
        print(f"Login Request Failed: {e}")

# 运行所有登录测试
print("Starting login tests for fixed phone login functionality...")

# 测试手机号登录（包含字母字符）
test_login(test_user['phone'], test_user['password'], "Phone (with letters)")

# 测试邮箱登录
test_login(test_user['email'], test_user['password'], "Email")

# 测试用户名登录
test_login(test_user['username'], test_user['password'], "Username")

print("\nAll login tests completed!")
