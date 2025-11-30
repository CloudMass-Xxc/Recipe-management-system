import requests
import json
import uuid

# 生成唯一的测试用户数据
test_suffix = str(uuid.uuid4())[:8]
new_user = {
    "username": f"testuser_{test_suffix}",
    "email": f"test_{test_suffix}@example.com",
    "phone": f"138{test_suffix[:6]}",  # 使用更真实的手机号格式
    "password": "password123"
}

BASE_URL = "http://localhost:8002/auth"

# 测试注册
def test_registration():
    url = f"{BASE_URL}/register"
    headers = {"Content-Type": "application/json"}
    
    print("\n=== Testing Registration ===")
    print(f"URL: {url}")
    print(f"User Data: {json.dumps(new_user, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=new_user)
        print(f"\nResponse Status Code: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"Response Body: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
            return response_data
        except json.JSONDecodeError:
            print(f"Response Body (not JSON): {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"\nRequest Failed: {e}")
        return None

# 测试登录
def test_login(identifier, password, identifier_type):
    url = f"{BASE_URL}/login"
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
            return response.status_code == 200
        except json.JSONDecodeError:
            print(f"Response Body (not JSON): {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Login Request Failed: {e}")
        return False

# 主测试流程
print("🚀 Starting Full Registration and Login Flow Test")
print(f"\n📋 Test User Data:")
print(f"   Username: {new_user['username']}")
print(f"   Email: {new_user['email']}")
print(f"   Phone: {new_user['phone']}")

# Step 1: Register a new user
print("\n🔄 Step 1: Registering new user...")
register_result = test_registration()

if register_result:
    print("\n✅ Registration successful!")
    
    # Step 2: Test all login methods
    print("\n🔄 Step 2: Testing all login methods...")
    
    # Get the actual phone number from registration response
    actual_phone = register_result.get('user', {}).get('phone')
    if actual_phone and actual_phone != new_user['phone']:
        print(f"\n📝 Note: Phone number was truncated during registration.")
        print(f"   Original: {new_user['phone']}")
        print(f"   Stored:   {actual_phone}")
    
    # Test 1: Login with username
    username_success = test_login(new_user['username'], new_user['password'], "Username")
    
    # Test 2: Login with email
    email_success = test_login(new_user['email'], new_user['password'], "Email")
    
    # Test 3: Login with phone (using the actual stored phone number)
    phone_success = test_login(actual_phone, new_user['password'], "Phone")
    
    # Summary
    print("\n📊 Test Results Summary:")
    print(f"- Username Login: {'✅' if username_success else '❌'}")
    print(f"- Email Login: {'✅' if email_success else '❌'}")
    print(f"- Phone Login: {'✅' if phone_success else '❌'}")
    
    if username_success and email_success and phone_success:
        print("\n🎉 All login methods are working correctly!")
    else:
        print("\n⚠️  Some login methods are still failing.")
else:
    print("\n❌ Registration failed. Cannot proceed with login tests.")

print("\n🏁 Test completed.")
