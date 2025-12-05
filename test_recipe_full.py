import requests
import json
import uuid

# 基础URL
BASE_URL = "http://localhost:8002"

def register_user():
    """注册新用户"""
    username = f"test_user_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    password = "Test@123"
    
    print(f"尝试注册用户: {username}")
    
    # 准备注册数据（不使用手机号，因为它是可选的）
    register_data = {
        "username": username,
        "email": email,
        "password": password
    }
    
    # 发送注册请求
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        headers={"Content-Type": "application/json"},
        json=register_data
    )
    
    if response.status_code == 200:
        print(f"✓ 用户注册成功: {username}")
        return username, password
    else:
        print(f"✗ 用户注册失败: {response.status_code}")
        print(f"错误信息: {response.json()}")
        return None, None

def login_user(username, password):
    """用户登录获取访问令牌"""
    print(f"尝试登录用户: {username}")
    
    # 准备登录数据
    login_data = {
        "username": username,
        "password": password
    }
    
    # 发送登录请求
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        headers={"Content-Type": "application/json"},
        json=login_data
    )
    
    if response.status_code == 200:
        data = response.json()
        access_token = data["data"]["access_token"]
        print("✓ 用户登录成功，获取到访问令牌")
        return access_token
    else:
        print(f"✗ 用户登录失败: {response.status_code}")
        print(f"错误信息: {response.json()}")
        return None

def generate_recipe(access_token):
    """使用访问令牌调用食谱生成API"""
    print("尝试生成个性化食谱...")
    
    # 准备食谱生成数据
    recipe_data = {
        "dietary_preferences": ["vegetarian"],
        "food_likes": ["番茄", "鸡蛋"],
        "food_dislikes": ["洋葱"],
        "health_conditions": [],
        "nutrition_goals": ["低卡路里"],
        "cooking_time_limit": 30,
        "difficulty": "easy",
        "cuisine": "chinese",
        "ingredients": ["番茄", "鸡蛋", "米饭"]
    }
    
    # 发送食谱生成请求
    response = requests.post(
        f"{BASE_URL}/ai/generate-recipe",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json=recipe_data
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✓ 食谱生成成功!")
        print("\n生成的食谱信息:")
        print(f"标题: {data.get('title')}")
        print(f"描述: {data.get('description')}")
        print(f"准备时间: {data.get('prep_time')} 分钟")
        print(f"烹饪时间: {data.get('cook_time')} 分钟")
        print(f"难度: {data.get('difficulty')}")
        print(f"菜系: {data.get('cuisine')}")
        print(f"卡路里: {data.get('calories')} kcal")
        print("\n食材列表:")
        for i, ingredient in enumerate(data.get('ingredients', []), 1):
            print(f"  {i}. {ingredient}")
        print("\n烹饪步骤:")
        for i, instruction in enumerate(data.get('instructions', []), 1):
            print(f"  {i}. {instruction}")
        return True
    else:
        print(f"✗ 食谱生成失败: {response.status_code}")
        print(f"错误信息: {response.json()}")
        return False

def test_recipe_generation():
    """测试完整的食谱生成流程"""
    print("=" * 50)
    print("开始测试个性化食谱生成功能")
    print("=" * 50)
    
    # 1. 注册用户
    username, password = register_user()
    if not username or not password:
        print("无法继续测试，用户注册失败")
        return False
    
    # 2. 用户登录
    access_token = login_user(username, password)
    if not access_token:
        print("无法继续测试，用户登录失败")
        return False
    
    # 3. 生成食谱
    success = generate_recipe(access_token)
    
    print("\n" + "=" * 50)
    if success:
        print("测试结果: ✓ 食谱生成功能测试成功!")
        print("✓ 我们的修复已经生效!")
    else:
        print("测试结果: ✗ 食谱生成功能测试失败")
    print("=" * 50)
    
    return success

if __name__ == "__main__":
    test_recipe_generation()
