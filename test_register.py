import requests
import json
import uuid

# 生成唯一的测试用户数据以避免冲突
test_suffix = str(uuid.uuid4())[:8]
# 生成随机手机号（模拟）
random_phone = f"13{test_suffix}"
new_user = {
    "username": f"testuser_{test_suffix}",
    "email": f"test_{test_suffix}@example.com",
    "phone": random_phone,  # 使用随机手机号避免冲突
    "password": "password123"
}

# 测试登录功能
def test_login(identifier, password):
    url = "http://localhost:8002/auth/login"
    headers = {"Content-Type": "application/json"}
    login_data = {"identifier": identifier, "password": password}
    
    print(f"\n=== Testing Login with {identifier} ===")
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

# 测试注册功能
def test_registration():
    url = "http://localhost:8002/auth/register"
    headers = {"Content-Type": "application/json"}
    
    print("\n=== Testing User Registration ===")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"User Data: {json.dumps(new_user, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=new_user)
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response Body: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        except json.JSONDecodeError:
            print(f"Response Body (not JSON): {response.text}")
            
        return response
    except requests.exceptions.RequestException as e:
        print(f"\nRequest Failed: {e}")
        return None

# 运行测试
response = test_registration()

# 分析结果
if response:
    if response.status_code == 201:
        print("\n✅ Registration Successful!")
        # 如果注册成功，立即测试登录
        test_login(response.json()['user']['username'], new_user['password'])
        test_login(new_user['email'], new_user['password'])
        test_login(new_user['phone'], new_user['password'])
    elif response.status_code == 400:
        print("\n❌ Registration Failed (Bad Request)")
        try:
            error_data = response.json()
            print(f"Error Message: {error_data.get('detail', 'Unknown error')}")
        except:
            print(f"Error: {response.text}")
    else:
        print(f"\n❌ Registration Failed with Status Code: {response.status_code}")
