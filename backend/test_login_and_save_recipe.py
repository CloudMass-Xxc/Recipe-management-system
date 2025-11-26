import requests
import json

# 登录信息
login_url = 'http://localhost:8001/auth/login'
login_data = {
    "identifier": "xxiaochang@qq.com",
    "password": "Xxc20001018..."
}

print("开始登录...")
print(f"登录URL: {login_url}")
print(f"登录数据: {json.dumps(login_data, ensure_ascii=False)}")

# 发送登录请求
try:
    login_response = requests.post(login_url, json=login_data)
    print(f"\n登录响应状态码: {login_response.status_code}")
    print(f"登录响应内容: {login_response.text}")
    
    # 检查登录是否成功
    if login_response.status_code == 200:
        login_result = login_response.json()
        token = login_result.get('access_token')
        print(f"\n获取到令牌: {token}")
        
        # 如果获取到了token，测试保存食谱功能
        if token:
            save_url = 'http://localhost:8001/ai/save-generated-recipe'
            recipe_data = {
                "recipe_data": {
                    "title": "测试食谱",
                    "description": "这是一个测试用的食谱",
                    "difficulty": "easy",
                    "cooking_time": 30,
                    "servings": 2,
                    "instructions": ["准备食材", "烹饪", "享用"],
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
            }
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            print(f"\n开始保存食谱...")
            print(f"保存URL: {save_url}")
            print(f"保存数据: {json.dumps(recipe_data, ensure_ascii=False, indent=2)}")
            
            # 发送保存食谱请求
            save_response = requests.post(save_url, json=recipe_data, headers=headers)
            print(f"\n保存食谱响应状态码: {save_response.status_code}")
            print(f"保存食谱响应内容: {save_response.text}")
    else:
        print(f"\n登录失败，状态码: {login_response.status_code}")
except Exception as e:
    print(f"\n发生错误: {e}")
