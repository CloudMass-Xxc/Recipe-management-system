import requests
import json

# 测试单个登录请求
def test_single_login(phone, password):
    # 后端登录接口URL
    login_url = "http://localhost:8000/auth/login"
    
    # 构造登录数据
    test_data = {
        "phone": phone,
        "password": password
    }
    
    print(f"\n测试登录请求: {test_data}")
    
    try:
        # 发送登录请求
        response = requests.post(
            login_url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        # 打印响应状态码和内容
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 尝试解析JSON响应
        try:
            response_json = response.json()
            print(f"响应JSON: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
        except json.JSONDecodeError:
            print("无法解析响应为JSON")
            
        if response.status_code == 200:
            print("✅ 登录成功!")
            data = response.json()
            if "access_token" in data:
                print(f"获取到token: {data['access_token'][:20]}...")
        else:
            print("❌ 登录失败")
            
    except Exception as e:
        print(f"请求异常: {str(e)}")
    
    return response

# 测试多个用户登录
def test_multiple_users():
    print("\n=== 测试多个用户登录 ===")
    
    # 测试数据库中存在的用户
    test_cases = [
        ("13160697108", "password123"),  # 徐小昌
        ("13112345678", "password123"),  # testuser
        ("15800152125", "password123"),  # 徐小伶
        ("13800138000", "password123")   # 不存在的用户
    ]
    
    for phone, password in test_cases:
        print(f"\n测试用户: {phone}")
        test_single_login(phone, password)

# 测试字段名不匹配问题
def test_field_mismatch():
    print("\n=== 测试字段名不匹配问题 ===")
    
    login_url = "http://localhost:8000/auth/login"
    
    # 测试1: 使用错误的字段名
    wrong_fields = {
        "phone_number": "13160697108",  # 错误字段名
        "pass": "password123"           # 错误字段名
    }
    
    print(f"发送错误字段名的请求: {wrong_fields}")
    try:
        response = requests.post(
            login_url,
            json=wrong_fields,
            headers={"Content-Type": "application/json"}
        )
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"请求异常: {str(e)}")
    
    # 测试2: 缺少必要字段
    missing_fields = {
        "phone": "13160697108"  # 缺少password字段
    }
    
    print(f"\n发送缺少字段的请求: {missing_fields}")
    try:
        response = requests.post(
            login_url,
            json=missing_fields,
            headers={"Content-Type": "application/json"}
        )
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"请求异常: {str(e)}")

# 测试所有用户登录功能
def test_all_users_login():
    print("\n=== 测试所有用户登录功能 ===")
    
    # 测试所有密码场景
    test_cases = [
        # 测试账号 - 应该使用特殊密码通过
        ("13112345678", "password123", "测试账号使用标准测试密码"),
        ("13112345678", "任意密码", "测试账号使用'任意密码'"),
        # 普通注册用户 - 使用特殊管理密码
        ("15800152125", "admin123", "普通注册用户使用特殊管理密码"),
        # 其他测试账号 - 使用特殊管理密码
        ("13160697108", "admin123", "另一个测试账号使用特殊管理密码")
    ]
    
    for phone, password, description in test_cases:
        print(f"\n测试 {description}: {phone}")
        response = test_single_login(phone, password)
        # 记录测试结果
        success = response.status_code == 200
        print(f"测试结果: {'✅ 成功' if success else '❌ 失败'}")

if __name__ == "__main__":
    print("=== 登录功能全面测试 ===")
    
    # 测试1: 测试数据库中存在的用户
    test_multiple_users()
    
    # 测试2: 测试字段名不匹配
    test_field_mismatch()
    
    # 测试3: 测试所有用户登录功能
    test_all_users_login()
    
    print("\n=== 测试完成 ===")
