import requests
import json
import time

# 测试注册API
def test_registration():
    url = 'http://localhost:8001/auth/register'
    headers = {'Content-Type': 'application/json'}
    
    # 使用时间戳生成唯一的用户名、邮箱和手机号
    timestamp = int(time.time())
    
    # 生成11位手机号：139开头，后面加上8位数字（使用时间戳的后8位）
    # 确保手机号是11位，格式符合^1[3-9]\d{9}$
    phone_suffix = str(timestamp % 100000000).zfill(8)  # 获取后8位，不足8位前面补0
    phone = f"139{phone_suffix}"
    
    data = {
        "username": f"testuser{timestamp}",
        "email": f"test{timestamp}@example.com",
        "phone": phone,
        "password": f"SecurePwd{timestamp}!",  # 使用更复杂的密码，包含时间戳避免常见模式
        "display_name": f"测试用户{timestamp}"
    }
    
    try:
        print(f"发送请求到: {url}")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 201:
            print("\n✅ 注册成功！")
        else:
            print("\n❌ 注册失败。")
            
    except Exception as e:
        print(f"\n❌ 请求异常: {str(e)}")

if __name__ == "__main__":
    test_registration()