import requests
import json
import time

BASE_URL = 'http://localhost:8001'
REGISTER_ENDPOINT = f'{BASE_URL}/auth/register'

print("🔍 开始验证注册功能")
print("="*50)

# 生成唯一的测试用户信息
timestamp = int(time.time())
test_user = {
    "username": f"verification_user_{timestamp}",
    "email": f"verification_{timestamp}@example.com",
    "phone": "13987654321",
    "password": "SecurePass789$XYZ",
    "display_name": f"测试用户_{timestamp}",
    "diet_preferences": []
}

print(f"📤 发送注册请求...")
print(f"用户数据: {json.dumps(test_user, ensure_ascii=False)}")

try:
    # 发送注册请求
    response = requests.post(
        REGISTER_ENDPOINT,
        json=test_user,
        headers={'Content-Type': 'application/json'},
        timeout=15
    )
    
    print(f"\n📥 收到响应")
    print(f"状态码: {response.status_code}")
    
    # 尝试解析JSON响应
    try:
        response_data = response.json()
        print(f"响应内容: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
    except json.JSONDecodeError:
        print(f"响应内容: {response.text}")
        response_data = None
    
    # 判断注册是否成功
    if response.status_code == 201 and response_data:
        print("\n✅ 注册成功！")
        print("\n📋 成功信息:")
        print(f"  用户ID: {response_data.get('user_id')}")
        print(f"  用户名: {response_data.get('username')}")
        print(f"  邮箱: {response_data.get('email')}")
        print(f"  手机号: {response_data.get('phone')}")
        print("\n🎉 注册功能验证通过！")
    else:
        print("\n❌ 注册失败！")
        if response.status_code == 422 and response_data:
            print("\n🔍 验证错误详情:")
            for error in response_data.get('detail', []):
                print(f"  - 字段: {'.'.join(map(str, error.get('loc', [])))}")
                print(f"    错误: {error.get('msg')}")
        else:
            print(f"\n🔍 错误详情: {response.text}")
            
except requests.exceptions.RequestException as e:
    print(f"\n❌ 请求异常: {str(e)}")
    print("💡 请检查后端服务是否正常运行")

except Exception as e:
    print(f"\n❌ 未知错误: {str(e)}")

print("\n" + "="*50)
print("✅ 验证完成！")
