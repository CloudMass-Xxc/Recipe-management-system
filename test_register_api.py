import requests
import json

# 测试基本URL
BASE_URL = "http://localhost:8002"

import random
import string

# 生成随机用户名
def generate_random_username(prefix="test_user", length=8):
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{prefix}_{suffix}"

# 生成随机电话号码
def generate_random_phone():
    # 生成13开头的随机11位电话号码
    return f"13{''.join(random.choices(string.digits, k=9))}"

# 测试用户数据
username = generate_random_username()
TEST_USER = {
    "username": username,
    "email": f"{username}@example.com",
    "phone": generate_random_phone(),
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

# 测试注册接口
def test_register_api():
    print("=== 直接测试后端注册API ===")
    url = f"{BASE_URL}/api/auth/register"
    print(f"测试URL: {url}")
    print(f"测试数据: {TEST_USER}")
    
    # 第一次注册尝试
    response = requests.post(url, json=TEST_USER)
    print_response(response)
    
    if response.status_code != 200:
        return False
    
    # 测试重复注册
    print("\n=== 测试重复注册场景 ===")
    print(f"使用相同的用户名再次注册: {TEST_USER['username']}")
    
    duplicate_response = requests.post(url, json=TEST_USER)
    print_response(duplicate_response)
    
    # 检查重复注册响应
    try:
        duplicate_data = duplicate_response.json()
        if duplicate_response.status_code == 400 and not duplicate_data.get('success'):
            print("\n✅ 重复注册测试通过！正确返回了400状态码和错误信息。")
            return True
        else:
            print("\n❌ 重复注册测试失败: 应该返回400状态码和失败信息")
            return False
    except Exception as e:
        print(f"\n❌ 解析重复注册响应时出错: {str(e)}")
        return False

# 运行测试
if __name__ == "__main__":
    print(f"开始测试后端注册API...")
    print(f"测试基本URL: {BASE_URL}")
    
    success = test_register_api()
    
    if success:
        print("\n✅ 后端注册API测试通过！")
    else:
        print("\n❌ 后端注册API测试失败！")
