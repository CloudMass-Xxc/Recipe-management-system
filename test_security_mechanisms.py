import requests
import time
import json
import sys
import random
import string

# 配置测试参数
BASE_URL = "http://localhost:8001"
FRONTEND_URL = "http://localhost:5174"

# 生成随机字符串
random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# 生成随机手机号
random_phone = f"138{random.randint(10000000, 99999999)}"

TEST_USER = {
    "username": f"test_security_user_{random_str}",
    "email": f"test_security_{random_str}@example.com",
    "phone": random_phone,
    "password": "Test123456",
    "display_name": "Test Security User"
}

# 测试函数
def test_security_mechanisms():
    print("\n" + "="*60)
    print("开始测试安全机制")
    print("="*60)
    
    # 1. 测试用户注册
    print("\n1. 测试用户注册...")
    register_response = requests.post(
        f"{BASE_URL}/auth/register",
        json=TEST_USER
    )
    
    if register_response.status_code == 201:
        print("✓ 用户注册成功")
        register_data = register_response.json()
        print(f"   访问令牌: {register_data['access_token'][:20]}...")
        print(f"   用户ID: {register_data['user']['user_id']}")
    else:
        print(f"✗ 用户注册失败: {register_response.status_code}")
        print(f"   响应: {register_response.text}")
        return
    
    # 2. 测试用户登录
    print("\n2. 测试用户登录...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "identifier": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
    )
    
    if login_response.status_code == 200:
        print("✓ 用户登录成功")
        login_data = login_response.json()
        access_token = login_data["access_token"]
        refresh_token = login_data.get("refresh_token")
        print(f"   访问令牌: {access_token[:20]}...")
        print(f"   刷新令牌: {refresh_token[:20]}..." if refresh_token else "   无刷新令牌")
    else:
        print(f"✗ 用户登录失败: {login_response.status_code}")
        print(f"   响应: {login_response.text}")
        return
    
    # 3. 测试获取用户信息（验证认证）
    print("\n3. 测试获取用户信息...")
    auth_headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = requests.get(
        f"{BASE_URL}/auth/me",
        headers=auth_headers
    )
    
    if user_info_response.status_code == 200:
        print("✓ 获取用户信息成功")
        user_info = user_info_response.json()
        print(f"   用户名: {user_info['username']}")
        print(f"   邮箱: {user_info['email']}")
    else:
        print(f"✗ 获取用户信息失败: {user_info_response.status_code}")
        print(f"   响应: {user_info_response.text}")
        return
    
    # 4. 测试刷新令牌
    if refresh_token:
        print("\n4. 测试刷新令牌...")
        refresh_response = requests.post(
            f"{BASE_URL}/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        if refresh_response.status_code == 200:
            print("✓ 刷新令牌成功")
            refresh_data = refresh_response.json()
            new_access_token = refresh_data["access_token"]
            print(f"   新访问令牌: {new_access_token[:20]}...")
        else:
            print(f"✗ 刷新令牌失败: {refresh_response.status_code}")
            print(f"   响应: {refresh_response.text}")
    
    # 5. 测试注销
    print("\n5. 测试用户注销...")
    logout_response = requests.post(
        f"{BASE_URL}/auth/logout",
        headers=auth_headers
    )
    
    if logout_response.status_code == 200:
        print("✓ 用户注销成功")
        print(f"   响应: {logout_response.json()['message']}")
    else:
        print(f"✗ 用户注销失败: {logout_response.status_code}")
        print(f"   响应: {logout_response.text}")
    
    # 6. 测试注销后令牌失效
    print("\n6. 测试注销后令牌失效...")
    expired_token_response = requests.get(
        f"{BASE_URL}/auth/me",
        headers=auth_headers
    )
    
    if expired_token_response.status_code == 401:
        print("✓ 注销后令牌正确失效")
    else:
        print(f"✗ 注销后令牌仍然有效: {expired_token_response.status_code}")
    
    print("\n" + "="*60)
    print("安全机制测试完成")
    print("="*60)
    print("\n测试说明:")
    print("1. 自动清除认证信息: 应用重启时，会话级存储的access_token会自动清除")
    print("2. 数据来源验证: 检查后端日志中是否有[DATA_SOURCE_VERIFICATION]前缀的日志")
    print("3. JWT增强验证: 包含令牌黑名单、JWT ID和版本验证")
    print("\n请手动检查:")
    print("- 后端日志中是否有数据来源验证的日志记录")
    print("- 重启前端应用后，认证状态是否自动清除")

if __name__ == "__main__":
    print("个性化食谱管理系统 - 安全机制测试脚本")
    print(f"测试环境: 后端={BASE_URL}, 前端={FRONTEND_URL}")
    
    try:
        test_security_mechanisms()
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
