import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

def login_get_token(phone, password):
    """
    登录获取token
    """
    login_url = f"{BASE_URL}/auth/login"
    login_data = {
        "phone": phone,
        "password": password
    }
    
    print(f"\n尝试登录: phone={phone}")
    try:
        response = requests.post(
            login_url,
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"✅ 登录成功，获取到token")
            return token
        else:
            print(f"❌ 登录失败: 状态码 {response.status_code}")
            print(f"响应内容: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 登录请求异常: {str(e)}")
        return None

def get_current_user_info(token):
    """
    使用token获取当前用户信息
    """
    me_url = f"{BASE_URL}/auth/me"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\n获取用户信息...")
    try:
        response = requests.get(me_url, headers=headers)
        
        if response.status_code == 200:
            user_info = response.json()
            print("✅ 获取用户信息成功")
            return user_info
        else:
            print(f"❌ 获取用户信息失败: 状态码 {response.status_code}")
            print(f"响应内容: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 获取用户信息请求异常: {str(e)}")
        return None

def display_user_info(user_info):
    """
    显示用户信息
    """
    if not user_info:
        return
    
    print("\n用户详细信息:")
    print("=" * 50)
    for key, value in user_info.items():
        # 格式化输出
        if isinstance(value, dict):
            print(f"{key}:")
            for k, v in value.items():
                print(f"  - {k}: {v}")
        else:
            print(f"{key}: {value}")
    print("=" * 50)

def main():
    print("通过API获取用户信息")
    print("-" * 30)
    
    # 测试使用测试手机号
    phone = "13160697108"
    password = "password123"  # 任意密码，测试模式下会跳过验证
    
    # 登录获取token
    token = login_get_token(phone, password)
    
    if token:
        # 获取用户信息
        user_info = get_current_user_info(token)
        
        # 显示用户信息
        if user_info:
            display_user_info(user_info)
    
    print("\n程序结束")

if __name__ == "__main__":
    main()