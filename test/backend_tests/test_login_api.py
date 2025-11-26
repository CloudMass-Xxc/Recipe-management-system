import requests
import json

# 测试登录API
def test_login():
    # 登录API URL (根据routes.py文件，正确路径是/auth/login)
    login_url = "http://localhost:8000/auth/login"
    
    # 使用我们刚刚创建的测试用户凭证
    login_data = {
        "phone": "13160697108",
        "password": "password123"
    }
    
    print(f"正在测试登录API: {login_url}")
    print(f"登录数据: {login_data}")
    
    try:
        # 发送登录请求
        response = requests.post(
            login_url,
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        # 打印响应状态码和内容
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        # 检查是否登录成功
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                print("\n🎉 登录成功！成功获取访问令牌。")
                print(f"访问令牌: {data['access_token'][:30]}...")
                return True
            else:
                print("\n❌ 登录失败: 响应中没有包含access_token")
                return False
        else:
            print(f"\n❌ 登录失败: 状态码 {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n⚠️ 请求异常: {e}")
        return False

# 运行测试
if __name__ == "__main__":
    print("=== 开始测试登录功能 ===")
    success = test_login()
    print("\n=== 测试结束 ===")
    print(f"测试结果: {'成功' if success else '失败'}")
