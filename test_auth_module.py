import requests
import json
import random
import string

# 后端API基础URL
BASE_URL = "http://localhost:8001/auth"

def generate_random_string(length=8):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_register():
    """测试用户注册功能"""
    print("\n=== 测试用户注册 ===")
    
    # 生成随机用户信息
    username = f"testuser_{generate_random_string()}"
    email = f"{username}@example.com"
    phone = f"138{random.randint(10000000, 99999999)}"
    password = "password123"
    display_name = f"Test User {generate_random_string()}"
    
    # 准备注册数据
    register_data = {
        "username": username,
        "email": email,
        "phone": phone,
        "password": password,
        "display_name": display_name
    }
    
    print(f"注册信息: {register_data}")
    
    # 发送注册请求
    response = requests.post(
        f"{BASE_URL}/register",
        headers={"Content-Type": "application/json"},
        data=json.dumps(register_data)
    )
    
    print(f"注册响应状态码: {response.status_code}")
    print(f"注册响应内容: {response.text}")
    
    if response.status_code == 201:
        print("✅ 注册成功!")
        return register_data, response.json()
    else:
        print("❌ 注册失败!")
        return None, None

def test_login(register_data):
    """测试用户登录功能"""
    print("\n=== 测试用户登录 ===")
    
    # 使用用户名登录
    login_data = {
        "identifier": register_data["username"],
        "password": register_data["password"]
    }
    
    print(f"登录信息: {login_data}")
    
    # 发送登录请求
    response = requests.post(
        f"{BASE_URL}/login",
        headers={"Content-Type": "application/json"},
        data=json.dumps(login_data)
    )
    
    print(f"登录响应状态码: {response.status_code}")
    print(f"登录响应内容: {response.text}")
    
    if response.status_code == 200:
        print("✅ 登录成功!")
        return response.json()
    else:
        print("❌ 登录失败!")
        return None

def test_get_me(login_response):
    """测试获取当前用户信息功能"""
    print("\n=== 测试获取当前用户信息 ===")
    
    if not login_response:
        print("❌ 登录失败，无法测试获取用户信息")
        return
    
    # 从登录响应中获取访问令牌
    access_token = login_response.get("access_token")
    
    if not access_token:
        print("❌ 登录响应中没有访问令牌")
        return
    
    # 发送获取用户信息请求
    response = requests.get(
        f"{BASE_URL}/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    
    print(f"获取用户信息响应状态码: {response.status_code}")
    print(f"获取用户信息响应内容: {response.text}")
    
    if response.status_code == 200:
        print("✅ 获取用户信息成功!")
        return response.json()
    else:
        print("❌ 获取用户信息失败!")
        return None

def test_duplicate_registration(register_data):
    """测试重复注册（用户名已存在）"""
    print("\n=== 测试重复注册（用户名已存在） ===")
    
    # 使用相同的用户名，不同的邮箱
    duplicate_data = {
        "username": register_data["username"],
        "email": f"different_{register_data['email']}",
        "phone": f"139{random.randint(10000000, 99999999)}",
        "password": "password456",
        "display_name": f"Duplicate User {generate_random_string()}"
    }
    
    print(f"重复注册信息: {duplicate_data}")
    
    # 发送注册请求
    response = requests.post(
        f"{BASE_URL}/register",
        headers={"Content-Type": "application/json"},
        data=json.dumps(duplicate_data)
    )
    
    print(f"重复注册响应状态码: {response.status_code}")
    print(f"重复注册响应内容: {response.text}")
    
    if response.status_code == 400:
        print("✅ 正确拒绝了重复用户名的注册!")
        return True
    else:
        print("❌ 没有正确拒绝重复用户名的注册!")
        return False

def test_invalid_login(register_data):
    """测试无效登录（密码错误）"""
    print("\n=== 测试无效登录（密码错误） ===")
    
    # 使用正确的用户名，错误的密码
    invalid_login_data = {
        "identifier": register_data["username"],
        "password": "wrong_password"
    }
    
    print(f"无效登录信息: {invalid_login_data}")
    
    # 发送登录请求
    response = requests.post(
        f"{BASE_URL}/login",
        headers={"Content-Type": "application/json"},
        data=json.dumps(invalid_login_data)
    )
    
    print(f"无效登录响应状态码: {response.status_code}")
    print(f"无效登录响应内容: {response.text}")
    
    if response.status_code == 401:
        print("✅ 正确拒绝了密码错误的登录!")
        return True
    else:
        print("❌ 没有正确拒绝密码错误的登录!")
        return False

if __name__ == "__main__":
    print("开始测试重新编写的注册登录模块...")
    
    # 测试注册
    register_data, register_response = test_register()
    
    if register_data:
        # 测试登录
        login_response = test_login(register_data)
        
        if login_response:
            # 测试获取当前用户信息
            get_me_response = test_get_me(login_response)
        
        # 测试重复注册
        test_duplicate_registration(register_data)
        
        # 测试无效登录
        test_invalid_login(register_data)
    
    print("\n测试完成!")
