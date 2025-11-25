import requests
import json

# 测试注册功能
def test_register():
    url = "http://localhost:8001/auth/register"
    
    # 测试数据 - 使用符合密码策略的密码（至少8位，包含大小写字母、数字和特殊字符）
    test_user = {
        "username": "testuser_new456",
        "email": "testuser_new456@example.com",
        "phone": "13900139001",
        "password": "Test123!",
        "display_name": "测试用户",
        "diet_preferences": []
    }
    
    print("发送注册请求...")
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_user)
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"完整响应内容: {response.text}")
        
        if response.status_code == 201:
            try:
                response_data = response.json()
                print("\n注册成功！响应数据:")
                print(f"访问令牌: {response_data.get('access_token')}")
                print(f"用户信息: {response_data.get('user')}")
                if response_data.get('user'):
                    print(f"用户ID: {response_data['user'].get('user_id')}")
                    print(f"用户名: {response_data['user'].get('username')}")
                    print(f"邮箱: {response_data['user'].get('email')}")
                    print(f"手机号: {response_data['user'].get('phone')}")
            except Exception as e:
                print(f"解析响应数据时出错: {str(e)}")
            return True
        else:
            try:
                error_data = response.json()
                print(f"\n注册失败: {error_data.get('detail', '未知错误')}")
            except:
                print(f"\n注册失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"请求异常: {str(e)}")
        return False

if __name__ == "__main__":
    print("===== 测试用户注册功能 =====")
    test_register()