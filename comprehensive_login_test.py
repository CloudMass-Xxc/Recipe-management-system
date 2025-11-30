import requests
import json
import time

# 测试配置
BASE_URL = "http://127.0.0.1:8001"
REGISTER_ENDPOINT = f"{BASE_URL}/auth/register"
LOGIN_ENDPOINT = f"{BASE_URL}/auth/login"
RECIPES_ENDPOINT = f"{BASE_URL}/recipes"
TEST_USER = {
    "email": "testuser@example.com",
    "username": "testuser",
    "identifier": "testuser@example.com",
    "password": "password123",
    "display_name": "Test User"
}

def test_register():
    """测试用户注册功能"""
    print("\n=== 测试用户注册功能 ===")
    try:
        # 准备注册数据（只包含必要字段）
        register_data = {
            "email": TEST_USER["email"],
            "username": TEST_USER["username"],
            "password": TEST_USER["password"],
            "display_name": TEST_USER["display_name"]
        }
        
        response = requests.post(REGISTER_ENDPOINT, json=register_data)
        print(f"注册请求状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("注册成功!")
            print(f"用户信息: {data}")
            return True
        else:
            print(f"注册结果: {response.text}")
            # 即使注册失败（比如用户已存在），我们也继续测试登录
            return False
    except Exception as e:
        print(f"注册测试异常: {e}")
        return False

def test_login():
    """测试用户登录功能"""
    print("\n=== 测试登录功能 ===")
    try:
        # 准备登录数据
        login_data = {
            "identifier": TEST_USER["identifier"],
            "password": TEST_USER["password"]
        }
        
        response = requests.post(LOGIN_ENDPOINT, json=login_data)
        print(f"登录请求状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("登录成功!")
            print(f"用户信息: {data.get('user')}")
            print(f"访问令牌: {data.get('access_token')}")
            return data.get('access_token')
        else:
            print(f"登录失败: {response.text}")
            return None
    except Exception as e:
        print(f"登录测试异常: {e}")
        return None

def test_get_recipes(token):
    """测试获取食谱列表"""
    print("\n=== 测试获取食谱列表 ===")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(RECIPES_ENDPOINT, headers=headers)
        print(f"获取食谱列表状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功获取食谱列表，共 {len(data)} 个食谱")
            if data:
                # 返回第一个食谱的ID，用于测试获取单个食谱
                return data[0].get('recipe_id')
        else:
            print(f"获取食谱列表失败: {response.text}")
        return None
    except Exception as e:
        print(f"获取食谱列表异常: {e}")
        return None

def test_get_recipe_detail(token, recipe_id):
    """测试获取单个食谱详情"""
    print("\n=== 测试获取单个食谱详情 ===")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{RECIPES_ENDPOINT}/{recipe_id}", headers=headers)
        print(f"获取食谱详情状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功获取食谱详情: {data.get('title')}")
            print(f"食谱作者: {data.get('author_name')}")
            print(f"烹饪时间: {data.get('cooking_time')} 分钟")
            print(f"难度: {data.get('difficulty')}")
            return True
        else:
            print(f"获取食谱详情失败: {response.text}")
            return False
    except Exception as e:
        print(f"获取食谱详情异常: {e}")
        return False

def test_unauthorized_access():
    """测试未授权访问"""
    print("\n=== 测试未授权访问 ===")
    try:
        # 不提供token访问受保护的资源
        response = requests.get(RECIPES_ENDPOINT)
        print(f"未授权访问状态码: {response.status_code}")
        
        if response.status_code == 401:
            print("未授权访问测试通过: 正确地返回了401错误")
            return True
        else:
            print(f"未授权访问测试失败: 期望401，实际得到{response.status_code}")
            return False
    except Exception as e:
        print(f"未授权访问测试异常: {e}")
        return False

def main():
    """运行所有测试"""
    print("开始全面登录测试...")
    print(f"测试环境: {BASE_URL}")
    
    # 测试未授权访问
    test_unauthorized_access()
    
    # 先注册用户
    test_register()
    
    # 测试登录
    token = test_login()
    
    if token:
        # 测试获取食谱列表
        recipe_id = test_get_recipes(token)
        
        if recipe_id:
            # 测试获取单个食谱详情
            test_get_recipe_detail(token, recipe_id)
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()