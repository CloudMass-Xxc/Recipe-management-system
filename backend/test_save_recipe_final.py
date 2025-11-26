import requests
import json
import sys

# 测试配置
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/auth/login"
SAVE_RECIPE_URL = f"{BASE_URL}/ai/save-generated-recipe"

# 用户凭据
USER_CREDENTIALS = {
    "identifier": "xuxiaochang@qq.com",  # 使用用户提供的邮箱
    "password": "Xxc20001018"  # 使用用户提供的密码
}

# 模拟的食谱数据，与前端生成的格式一致
sample_recipe_data = {
    "title": "测试食谱",
    "description": "这是一个测试用的食谱",
    "difficulty": "easy",
    "cooking_time": 30,
    "prep_time": 15,
    "servings": 2,
    "instructions": ["准备食材", "烹饪", "享用"],
    "tips": ["可以根据个人口味调整调味料"],
    "nutrition_info": {
        "calories": 500,
        "protein": 20,
        "carbs": 60,
        "fat": 15,
        "fiber": 5
    },
    "ingredients": [
        {
            "name": "鸡蛋",
            "quantity": 2,
            "unit": "个",
            "note": "新鲜"
        },
        {
            "name": "米饭",
            "quantity": 1,
            "unit": "碗",
            "note": "煮熟"
        }
    ],
    "tags": ["测试", "快速"]
}

def test_save_recipe_functionality():
    """测试保存食谱功能"""
    print("开始测试 '添加到我的食谱' 功能...\n")
    
    # 1. 登录获取令牌
    print(f"1. 尝试登录用户: {USER_CREDENTIALS['identifier']}")
    try:
        login_response = requests.post(LOGIN_URL, json=USER_CREDENTIALS)
        print(f"   登录响应状态码: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            access_token = login_data.get('access_token')
            if access_token:
                print("   登录成功，获取到访问令牌！")
            else:
                print("   登录成功，但未获取到访问令牌。")
                print(f"   登录响应内容: {login_data}")
                return False
        else:
            print(f"   登录失败: {login_response.status_code}")
            try:
                error_data = login_response.json()
                print(f"   错误信息: {error_data}")
            except:
                print(f"   响应内容: {login_response.text}")
            return False
    except Exception as e:
        print(f"   登录请求异常: {str(e)}")
        return False
    
    # 2. 构建请求头和请求体
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    request_body = {
        "recipe_data": sample_recipe_data,
        "share_with_community": False
    }
    
    # 3. 调用保存食谱API
    print("\n2. 尝试保存食谱到用户账户")
    print(f"   请求URL: {SAVE_RECIPE_URL}")
    print(f"   请求头: {json.dumps(headers, indent=2)}")
    print(f"   请求体: {json.dumps(request_body, indent=2)}")
    
    try:
        save_response = requests.post(SAVE_RECIPE_URL, json=request_body, headers=headers)
        print(f"\n3. 保存食谱响应状态码: {save_response.status_code}")
        
        if save_response.status_code == 200:
            save_data = save_response.json()
            print("   保存食谱成功！")
            print(f"   保存的食谱ID: {save_data.get('recipe_id')}")
            print(f"   完整响应内容: {json.dumps(save_data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"   保存食谱失败: {save_response.status_code}")
            try:
                error_data = save_response.json()
                print(f"   错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   响应内容: {save_response.text}")
            return False
    except Exception as e:
        print(f"   保存食谱请求异常: {str(e)}")
        return False

# 运行测试
if __name__ == "__main__":
    print("========== '添加到我的食谱' 功能测试 ==========\n")
    
    success = test_save_recipe_functionality()
    
    print("\n========== 测试结果 ==========")
    if success:
        print("✅ 测试通过: '添加到我的食谱' 功能正常工作！")
        sys.exit(0)
    else:
        print("❌ 测试失败: '添加到我的食谱' 功能存在问题。")
        sys.exit(1)
