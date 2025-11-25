import requests
import json

# 测试登录功能
def test_login():
    print("开始测试登录功能...")
    
    # 登录API地址
    login_url = "http://localhost:8001/auth/login"
    
    # 测试账号信息（使用identifier字段）
    test_credentials = {
        "identifier": "testuser_new456",  # 可以是手机号、邮箱或用户名
        "password": "Test123!"
    }
    
    try:
        # 发送登录请求
        print(f"发送登录请求到: {login_url}")
        print(f"测试账号: {test_credentials}")
        
        response = requests.post(login_url, json=test_credentials)
        print(f"响应状态码: {response.status_code}")
        print(f"完整响应内容: {response.text}")
        try:
            response_data = response.json()
            print(f"响应内容 (JSON解析后): {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        except Exception as e:
            print(f"解析响应JSON时出错: {str(e)}")
        
        # 检查是否登录成功
        if response.status_code == 200:
            token = response.json().get("access_token")
            if token:
                print("✅ 登录成功！已获取访问令牌")
                
                # 使用token获取用户信息
                me_url = "http://localhost:8001/auth/me"
                headers = {"Authorization": f"Bearer {token}"}
                
                me_response = requests.get(me_url, headers=headers)
                print(f"获取用户信息状态码: {me_response.status_code}")
                print(f"用户信息: {json.dumps(me_response.json(), ensure_ascii=False, indent=2)}")
                
                if me_response.status_code == 200:
                    print("✅ 获取用户信息成功！")
                else:
                    print("❌ 获取用户信息失败")
            else:
                print("❌ 登录响应中未包含access_token")
        else:
            print("❌ 登录失败")
            
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    test_login()