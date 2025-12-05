import requests
import json

# 测试基本URL
BASE_URL = "http://localhost:8002"

# 测试用户数据 - 使用新的用户名和邮箱，避免冲突
TEST_USER = {
    "username": "test_full_flow",
    "email": "test_full_flow@example.com",
    "phone": "13800138003",
    "password": "Test123456!"
}

def print_response(response):
    """打印响应信息"""
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    try:
        response_data = response.json()
        print(f"响应内容 (JSON解析后): {json.dumps(response_data, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"解析响应JSON时出错: {str(e)}")

# 测试完整的注册和登录流程
def test_full_register_login_flow():
    print("=== 测试完整的注册和登录流程 ===")
    
    # 步骤1: 测试注册
    print("\n--- 步骤1: 测试用户注册 ---")
    register_url = f"{BASE_URL}/api/auth/register"
    print(f"注册URL: {register_url}")
    print(f"注册数据: {TEST_USER}")
    
    register_response = requests.post(register_url, json=TEST_USER)
    print_response(register_response)
    
    if register_response.status_code != 200:
        print("❌ 注册失败，终止测试！")
        return False
    
    # 步骤2: 测试使用相同的用户名和密码登录
    print("\n--- 步骤2: 测试用户登录 ---")
    login_url = f"{BASE_URL}/api/auth/login"
    login_data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    }
    print(f"登录URL: {login_url}")
    print(f"登录数据: {login_data}")
    
    login_response = requests.post(login_url, json=login_data)
    print_response(login_response)
    
    if login_response.status_code != 200:
        print("❌ 登录失败，终止测试！")
        return False
    
    # 步骤3: 测试使用邮箱登录
    print("\n--- 步骤3: 测试使用邮箱登录 ---")
    email_login_data = {
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    print(f"登录URL: {login_url}")
    print(f"邮箱登录数据: {email_login_data}")
    
    email_login_response = requests.post(login_url, json=email_login_data)
    print_response(email_login_response)
    
    if email_login_response.status_code != 200:
        print("❌ 使用邮箱登录失败！")
        return False
    
    # 步骤4: 测试使用手机号登录
    print("\n--- 步骤4: 测试使用手机号登录 ---")
    phone_login_data = {
        "username": TEST_USER["phone"],
        "password": TEST_USER["password"]
    }
    print(f"登录URL: {login_url}")
    print(f"手机号登录数据: {phone_login_data}")
    
    phone_login_response = requests.post(login_url, json=phone_login_data)
    print_response(phone_login_response)
    
    if phone_login_response.status_code != 200:
        print("❌ 使用手机号登录失败！")
        return False
    
    print("\n🎉 完整的注册和登录流程测试通过！")
    return True

# 运行测试
if __name__ == "__main__":
    print("开始测试完整的注册和登录流程...")
    print(f"测试基本URL: {BASE_URL}")
    
    success = test_full_register_login_flow()
    
    if success:
        print("\n✅ 所有测试通过！认证功能修复成功！")
    else:
        print("\n❌ 测试失败！认证功能仍有问题！")
