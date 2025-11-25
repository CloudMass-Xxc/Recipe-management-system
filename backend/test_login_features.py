import requests
import json

BASE_URL = "http://localhost:8000/auth"

# 测试数据 - 使用新的测试账号
test_user = {
    "username": "test_login_user2",
    "email": "test_login_user2@example.com",
    "phone": "13700137001",
    "password": "test123",
    "display_name": "测试登录用户2"
}

def test_register_with_required_phone():
    """测试注册功能，验证手机号是必选项"""
    print("\n===== 测试注册功能（手机号必选）=====")
    
    # 测试缺少手机号的情况
    user_without_phone = test_user.copy()
    del user_without_phone["phone"]
    
    print("发送缺少手机号的注册请求...")
    response = requests.post(f"{BASE_URL}/register", json=user_without_phone)
    
    print(f"响应状态码: {response.status_code}")
    if response.status_code != 201:
        print(f"预期结果：缺少手机号时应返回错误")
        print(f"实际结果：{response.text}")
    else:
        print("测试失败：缺少手机号时不应成功注册")
        return False
    
    # 正常注册测试（包含手机号）
    print("\n发送完整的注册请求...")
    response = requests.post(f"{BASE_URL}/register", json=test_user)
    
    print(f"响应状态码: {response.status_code}")
    if response.status_code == 201:
        print("注册成功！")
        data = response.json()
        print(f"用户ID: {data.get('user_id')}")
        print(f"用户名: {data.get('username')}")
        print(f"邮箱: {data.get('email')}")
        print(f"手机号: {data.get('phone')}")
        return True
    else:
        print(f"注册失败: {response.text}")
        return False

def test_login_with_multiple_methods():
    """测试使用不同方式登录"""
    print("\n===== 测试多种登录方式 =====")
    
    # 1. 使用用户名登录
    print("\n1. 使用用户名登录...")
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    print(f"响应状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"使用用户名登录成功！Token: {data.get('access_token')[:20]}...")
    else:
        print(f"使用用户名登录失败: {response.text}")
        return False
    
    # 2. 使用邮箱登录
    print("\n2. 使用邮箱登录...")
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    print(f"响应状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"使用邮箱登录成功！Token: {data.get('access_token')[:20]}...")
    else:
        print(f"使用邮箱登录失败: {response.text}")
        return False
    
    # 3. 使用手机号登录
    print("\n3. 使用手机号登录...")
    login_data = {
        "phone": test_user["phone"],
        "password": test_user["password"]
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    print(f"响应状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"使用手机号登录成功！Token: {data.get('access_token')[:20]}...")
        return True
    else:
        print(f"使用手机号登录失败: {response.text}")
        return False

if __name__ == "__main__":
    print("开始测试注册和登录功能...")
    
    # 先测试注册功能
    register_success = test_register_with_required_phone()
    
    if register_success:
        # 如果注册成功，测试多种登录方式
        login_success = test_login_with_multiple_methods()
        
        if login_success:
            print("\n===== 所有测试通过！=====")
        else:
            print("\n===== 登录测试失败！=====")
    else:
        print("\n===== 注册测试失败！=====")
