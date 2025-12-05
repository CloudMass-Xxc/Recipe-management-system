import requests
import json
import sys

# 设置测试环境
BASE_URL = "http://localhost:8002"

# 测试数据
TEST_USER = {
    "username": "testuser123",
    "email": "test@example.com",
    "phone": "13800138000",
    "password": "password123"
}

LOGIN_DATA = {
    "username": TEST_USER["username"],
    "password": TEST_USER["password"]
}

def print_response(response):
    """打印响应信息"""
    print(f"状态码: {response.status_code}")
    try:
        data = response.json()
        print("响应内容:")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except json.JSONDecodeError:
        print("响应内容: (非JSON格式)")
        print(response.text)
    print("-" * 50)

def test_register():
    """测试用户注册功能"""
    print("\n=== 测试用户注册 ===")
    url = f"{BASE_URL}/api/auth/register"
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
    response = requests.post(url, json=LOGIN_DATA)
    print_response(response)
    
    if response.status_code == 200:
        print("✅ 用户登录测试通过！")
        # 返回访问令牌
        return response.json().get("data", {}).get("access_token")
    else:
        print("❌ 用户登录测试失败！")
        return None

def test_get_current_user(access_token):
    """测试获取当前用户信息功能"""
    print("\n=== 测试获取当前用户信息 ===")
    if not access_token:
        print("❌ 没有访问令牌，跳过此测试！")
        return False
    
    url = f"{BASE_URL}/api/auth/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        print("✅ 获取当前用户信息测试通过！")
        return True
    else:
        print("❌ 获取当前用户信息测试失败！")
        return False

def main():
    """主测试函数"""
    print("开始测试重构后的注册登录功能...")
    print(f"测试环境: {BASE_URL}")
    print("=" * 60)
    
    success = True
    
    # 1. 测试注册
    if not test_register():
        success = False
    
    # 2. 测试登录
    access_token = test_login()
    if not access_token:
        success = False
    
    # 3. 测试获取用户信息
    if access_token:
        if not test_get_current_user(access_token):
            success = False
    
    # 总结测试结果
    print("\n" + "=" * 60)
    if success:
        print("🎉 所有测试通过！重构后的注册登录功能正常工作！")
        return 0
    else:
        print("💥 部分测试失败！请检查代码实现。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
