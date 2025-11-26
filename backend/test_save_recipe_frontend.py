import requests
import json

# 登录信息
login_data = {
    "identifier": "xxiaochang@qq.com",
    "password": "Xxc20001018..."
}

# 登录获取令牌
def get_token():
    print("正在登录...")
    response = requests.post(
        "http://localhost:8000/auth/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"登录成功，获取到令牌: {token}")
        return token
    else:
        print(f"登录失败，状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        return None

# 模拟前端发送的食谱数据
def get_recipe_data():
    # 这是模拟前端生成的食谱数据，与RecipeGeneratorPage.tsx中的格式一致
    return {
        "title": "测试食谱",
        "description": "这是一个测试用的食谱",
        "difficulty": "easy",
        "cooking_time": 30,
        "prep_time": 10,
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

# 测试保存食谱功能
def test_save_recipe(token):
    if not token:
        print("没有获取到令牌，无法测试保存食谱功能")
        return
    
    print("准备保存食谱...")
    recipe_data = get_recipe_data()
    
    # 构建请求体，与前端RecipeAPI.saveGeneratedRecipe方法中的格式一致
    request_body = {
        "recipe_data": recipe_data,
        "share_with_community": False
    }
    
    print("保存食谱请求体:")
    print(json.dumps(request_body, ensure_ascii=False, indent=2))
    
    response = requests.post(
        "http://localhost:8000/ai/save-generated-recipe",
        json=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )
    
    print(f"保存食谱响应状态码: {response.status_code}")
    print(f"保存食谱响应内容:")
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    
    if response.status_code == 200:
        print("保存食谱成功！")
    else:
        print("保存食谱失败！")

# 运行测试
if __name__ == "__main__":
    token = get_token()
    test_save_recipe(token)
