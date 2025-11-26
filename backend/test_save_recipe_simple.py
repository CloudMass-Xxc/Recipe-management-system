import requests
import json
import uuid

# 配置
base_url = "http://localhost:8000"
register_url = f"{base_url}/auth/register"
login_url = f"{base_url}/auth/login"
save_recipe_url = f"{base_url}/ai/save-generated-recipe"

# 生成唯一的测试用户名（避免重复）
test_username = f"test_user_{uuid.uuid4().hex[:8]}"
test_email = f"{test_username}@example.com"

# 测试用户注册数据
user_register_data = {
    "username": test_username,
    "email": test_email,
    "password": "Test123456",
    "display_name": "测试用户"
}

# 测试用户登录凭据
user_credentials = {
    "identifier": test_email,
    "password": "Test123456"
}

# 测试食谱数据
test_recipe = {
    "title": "测试食谱",
    "description": "这是一个测试用的食谱",
    "difficulty": "easy",
    "prep_time": 10,  # 添加必填的准备时间
    "cooking_time": 30,
    "servings": 2,
    "instructions": ["准备食材", "烹饪", "享用"],  # 改为字符串列表
    "ingredients": [
        {"name": "鸡蛋", "quantity": 2, "unit": "个", "note": "新鲜"},
        {"name": "米饭", "quantity": 1, "unit": "碗", "note": "煮熟"}
    ],
    "tags": ["测试", "快速"],
    "nutrition_info": {
        "calories": 500,
        "protein": 20,
        "carbs": 60,
        "fat": 15,
        "fiber": 5
    }
}

try:
    print("=== 开始测试保存食谱功能 ===")
    
    # 0. 先注册测试用户
    print("\n0. 正在注册测试用户...")
    register_response = requests.post(register_url, json=user_register_data)
    print(f"注册响应状态码: {register_response.status_code}")
    print(f"注册响应内容: {register_response.text}")
    
    if register_response.status_code == 201:
        print(f"\n✅ 测试用户注册成功: {test_username}")
        
        # 1. 登录获取令牌
        print("\n1. 正在登录...")
        login_response = requests.post(login_url, json=user_credentials)
        print(f"登录响应状态码: {login_response.status_code}")
        print(f"登录响应内容: {login_response.text}")
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            access_token = login_data.get("access_token")
            print(f"成功获取访问令牌: {access_token[:20]}...")
            
            # 2. 保存食谱
            print("\n2. 正在保存食谱...")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            save_recipe_data = {
                "recipe_data": test_recipe,
                "share_with_community": False
            }
            
            save_response = requests.post(
                save_recipe_url,
                json=save_recipe_data,
                headers=headers
            )
            
            print(f"保存食谱响应状态码: {save_response.status_code}")
            print(f"保存食谱响应内容: {save_response.text}")
            
            if save_response.status_code == 200:
                print("\n✅ 测试成功！食谱保存功能正常工作。")
            else:
                print("\n❌ 测试失败！食谱保存失败。")
        else:
            print("\n❌ 登录失败")
            print("\n测试终止。")
    else:
        print("\n❌ 用户注册失败")
        print("\n测试终止。")
        
except Exception as e:
    print(f"\n❌ 测试过程中发生错误: {str(e)}")

print("\n=== 测试结束 ===")
