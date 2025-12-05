import requests
import json

# 测试配置
BASE_URL = "http://localhost:8000/api"
LOGIN_URL = f"{BASE_URL}/auth/login"
GENERATE_RECIPE_URL = f"{BASE_URL}/ai/generate-recipe"

# 测试用户凭据
TEST_USERNAME = "testuser2"
TEST_EMAIL = "test2@example.com"
TEST_PHONE = "13900139000"
TEST_PASSWORD = "Test123!"

def test_recipe_generation():
    print("🎯 ========== 测试食谱生成API功能 ==========")
    print("开始测试食谱生成API功能...\n")
    
    try:
        # 步骤1: 登录获取token
        print("🔍 步骤1：用户登录获取认证Token")
        login_payload = {
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }
        
        print(f"   📊 登录请求URL: {LOGIN_URL}")
        print(f"   📋 登录请求参数: {json.dumps(login_payload, ensure_ascii=False)}")
        
        login_response = requests.post(LOGIN_URL, json=login_payload)
        
        print(f"   📊 登录响应状态码: {login_response.status_code}")
        print(f"   📝 登录响应内容: {login_response.text}")
        
        if login_response.status_code != 200:
            print(f"   ❌ 登录失败: 状态码 {login_response.status_code}")
            return False
        
        login_data = login_response.json()
        print(f"   📋 登录响应解析后的数据: {json.dumps(login_data, ensure_ascii=False)}")
        
        # 检查响应数据结构，尝试从不同的键获取token
        token = login_data.get("access_token")
        if not token:
            token = login_data.get("data", {}).get("access_token")
        
        if not token:
            print("   ❌ 未获取到认证Token")
            print(f"   ❓ 响应数据中的可用键: {list(login_data.keys())}")
            return False
        
        print("   ✅ 登录成功，获取到认证Token")
        
        # 步骤2: 使用token调用食谱生成API
        print("\n🔍 步骤2：调用食谱生成API")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        recipe_payload = {
            "ingredients": ["鸡蛋", "西红柿", "面条"],
            "cooking_time": 30,
            "servings": 2,
            "difficulty": "easy",
            "cuisine": "chinese",
            "dietary_preferences": ["none"],
            "allergies": [],
            "include_image": False
        }
        
        print(f"   📋 请求参数: {json.dumps(recipe_payload, ensure_ascii=False)}")
        
        recipe_response = requests.post(GENERATE_RECIPE_URL, json=recipe_payload, headers=headers)
        
        print(f"   📊 响应状态码: {recipe_response.status_code}")
        print(f"   📝 响应内容: {recipe_response.text}")
        
        if recipe_response.status_code != 200:
            print("   ❌ 食谱生成失败")
            return False
        
        recipe_data = recipe_response.json()
        
        # 验证响应数据结构
        if not all(key in recipe_data for key in ["recipe_id", "title", "description", "instructions", "ingredients"]):
            print("   ❌ 响应数据结构不完整")
            return False
        
        print("   ✅ 食谱生成成功！")
        print(f"   🎉 生成的食谱标题: {recipe_data['title']}")
        print(f"   📝 食谱描述: {recipe_data['description']}")
        print(f"   👩🍳 烹饪步骤数: {len(recipe_data['instructions'])}")
        print(f"   🥘 食材数量: {len(recipe_data['ingredients'])}")
        
        print("\n🏁 ========== 测试结果汇总 ==========")
        print("✅ 测试通过！食谱生成API功能正常工作。")
        return True
        
    except Exception as e:
        print(f"\n💥 测试过程中发生错误: {str(e)}")
        print("\n🏁 ========== 测试结果汇总 ==========")
        print("❌ 测试失败！食谱生成API功能存在问题。")
        import traceback
        print(f"\n错误详情:\n{traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_recipe_generation()
