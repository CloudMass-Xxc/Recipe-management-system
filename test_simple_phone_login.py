import requests
import json

# 使用简单的纯数字手机号进行测试
test_user = {
    "username": "test_simple_phone",
    "email": "test_simple@example.com",
    "phone": "13800138000",  # 纯数字手机号
    "password": "password123"
}

BASE_URL = "http://localhost:8002/auth"

# 先检查用户是否已存在，如果存在则跳过注册
def check_and_register():
    print("\n=== Checking if test user exists ===")
    
    # 尝试用手机号登录，如果成功则用户已存在
    url = f"{BASE_URL}/login"
    headers = {"Content-Type": "application/json"}
    login_data = {"identifier": test_user['phone'], "password": test_user['password']}
    
    response = requests.post(url, headers=headers, json=login_data)
    if response.status_code == 200:
        print("✅ Test user already exists. Using existing user.")
        return True
    
    # 尝试用邮箱登录检查
    login_data['identifier'] = test_user['email']
    response = requests.post(url, headers=headers, json=login_data)
    if response.status_code == 200:
        print("✅ Test user already exists. Using existing user.")
        return True
    
    # 如果用户不存在，进行注册
    print("\n=== Registering new test user ===")
    url = f"{BASE_URL}/register"
    response = requests.post(url, headers=headers, json=test_user)
    
    print(f"Response Status Code: {response.status_code}")
    try:
        response_data = response.json()
        print(f"Response Body: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        return response.status_code == 201
    except json.JSONDecodeError:
        print(f"Response Body (not JSON): {response.text}")
        return False

# 测试登录
def test_login(identifier, password, identifier_type):
    url = f"{BASE_URL}/login"
    headers = {"Content-Type": "application/json"}
    login_data = {"identifier": identifier, "password": password}
    
    print(f"\n=== Testing Login with {identifier_type} ===")
    print(f"URL: {url}")
    print(f"Login Data: {json.dumps(login_data, ensure_ascii=False)}")
    
    response = requests.post(url, headers=headers, json=login_data)
    print(f"Response Status Code: {response.status_code}")
    
    try:
        response_data = response.json()
        print(f"Response Body: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except json.JSONDecodeError:
        print(f"Response Body (not JSON): {response.text}")
        return False

# 主测试流程
print("🚀 Starting Simple Phone Login Test")
print(f"\n📋 Test User Data:")
print(f"   Username: {test_user['username']}")
print(f"   Email: {test_user['email']}")
print(f"   Phone: {test_user['phone']} (Pure digits)")

# Step 1: Register user if needed
if check_and_register():
    # Step 2: Test all login methods
    print("\n🔄 Step 2: Testing all login methods with pure digit phone...")
    
    # Test 1: Login with username
    username_success = test_login(test_user['username'], test_user['password'], "Username")
    
    # Test 2: Login with email
    email_success = test_login(test_user['email'], test_user['password'], "Email")
    
    # Test 3: Login with phone (pure digits)
    phone_success = test_login(test_user['phone'], test_user['password'], "Phone")
    
    # Summary
    print("\n📊 Test Results Summary:")
    print(f"- Username Login: {'✅' if username_success else '❌'}")
    print(f"- Email Login: {'✅' if email_success else '❌'}")
    print(f"- Phone Login: {'✅' if phone_success else '❌'}")
    
    if username_success and email_success and phone_success:
        print("\n🎉 All login methods are working correctly!")
    else:
        print("\n⚠️  Some login methods are still failing.")
        
        # 诊断信息
        print("\n🔍 Diagnostic Information:")
        print("- User exists and can be found by username/email")
        print("- Phone number is pure digits (13800138000)")
        print("- Login logic should prioritize phone number lookup")
        print("- If phone login fails but others work, check:")
        print("  1. Database phone field storage")
        print("  2. Phone field indexing")
        print("  3. Login route phone lookup logic")
else:
    print("\n❌ Failed to create or find test user.")

print("\n🏁 Test completed.")
