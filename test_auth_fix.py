import requests
import json
import time

# 测试基本URL
BASE_URL = "http://localhost:8002"

# 测试用户数据
TEST_USER = {
    "username": "test_user_fix",
    "email": "test_fix@example.com",
    "phone": "13800138001",
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

def test_register():
    """测试用户注册功能"""
    print("\n=== 测试用户注册 ===")
    url = f"{BASE_URL}/api/auth/register"
    print(f"发送注册请求到: {url}")
    print(f"测试用户数据: {TEST_USER}")
    
    response = requests.post(url, json=TEST_USER)
    print_response(response)
    
    if response.status_code == 200:
        print("✅ 用户注册测试通过！")
        return True
    else:
        print("❌ 用户注册测试失败！")
        return False

def test_login():
    """测试用户登录功能"""
    print("\n=== 测试用户登录 ===")
    url = f"{BASE_URL}/api/auth/login"
    
    # 测试使用用户名登录
    print("\n--- 使用用户名登录 ---")
    login_data = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    }
    print(f"发送登录请求到: {url}")
    print(f"登录数据: {login_data}")
    
    response = requests.post(url, json=login_data)
    print_response(response)
    
    if response.status_code == 200:
        print("✅ 使用用户名登录测试通过！")
        return True
    else:
        print("❌ 使用用户名登录测试失败！")
        return False

def test_login_with_email():
    """测试使用邮箱登录"""
    print("\n--- 使用邮箱登录 ---")
    url = f"{BASE_URL}/api/auth/login"
    login_data = {
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    print(f"发送登录请求到: {url}")
    print(f"登录数据: {login_data}")
    
    response = requests.post(url, json=login_data)
    print_response(response)
    
    if response.status_code == 200:
        print("✅ 使用邮箱登录测试通过！")
        return True
    else:
        print("❌ 使用邮箱登录测试失败！")
        return False

def test_login_with_phone():
    """测试使用手机号登录"""
    print("\n--- 使用手机号登录 ---")
    url = f"{BASE_URL}/api/auth/login"
    login_data = {
        "username": TEST_USER["phone"],
        "password": TEST_USER["password"]
    }
    print(f"发送登录请求到: {url}")
    print(f"登录数据: {login_data}")
    
    response = requests.post(url, json=login_data)
    print_response(response)
    
    if response.status_code == 200:
        print("✅ 使用手机号登录测试通过！")
        return True
    else:
        print("❌ 使用手机号登录测试失败！")
        return False

# 运行测试
if __name__ == "__main__":
    print("开始测试认证功能修复...")
    print(f"测试基本URL: {BASE_URL}")
    
    # 测试注册
    register_success = test_register()
    
    if register_success:
        # 等待一点时间，确保数据已保存
        time.sleep(1)
        
        # 测试登录
        login_success = test_login()
        
        if login_success:
            # 测试使用邮箱和手机号登录
            email_login_success = test_login_with_email()
            phone_login_success = test_login_with_phone()
            
            if email_login_success and phone_login_success:
                print("\n🎉 所有认证功能测试通过！")
            else:
                print("\n❌ 部分认证功能测试失败！")
        else:
            print("\n❌ 登录功能测试失败！")
    else:
        print("\n❌ 注册功能测试失败！")
