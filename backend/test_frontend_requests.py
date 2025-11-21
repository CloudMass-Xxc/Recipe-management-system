import requests
import json
import time

# 后端API地址
API_URL = "http://localhost:8000/ai/generate-recipe"

def test_frontend_style_requests():
    """模拟前端的实际请求格式进行测试"""
    print("开始模拟前端请求测试...")
    
    # 模拟前端可能发送的各种请求场景
    test_scenarios = [
        {
            "name": "场景1: 完整参数（应该成功）",
            "params": {
                "dietary_preferences": [],
                "food_likes": ["西红柿", "鸡蛋", "米饭"],
                "food_dislikes": [],
                "health_conditions": [],
                "nutrition_goals": [],
                "cooking_time_limit": 30,
                "difficulty": "easy",
                "cuisine": "chinese"
            }
        },
        {
            "name": "场景2: 空难度值（应该成功）",
            "params": {
                "dietary_preferences": [],
                "food_likes": ["鸡肉", "土豆"],
                "food_dislikes": [],
                "health_conditions": [],
                "nutrition_goals": [],
                "cooking_time_limit": 45,
                "difficulty": None,
                "cuisine": "chinese"
            }
        },
        {
            "name": "场景3: 素食偏好",
            "params": {
                "dietary_preferences": ["vegetarian"],
                "food_likes": ["蔬菜", "豆腐"],
                "food_dislikes": [],
                "health_conditions": [],
                "nutrition_goals": [],
                "cooking_time_limit": None,
                "difficulty": "medium",
                "cuisine": "chinese"
            }
        },
        {
            "name": "场景4: 所有可选参数为空",
            "params": {
                "dietary_preferences": [],
                "food_likes": ["牛肉"],
                "food_dislikes": [],
                "health_conditions": [],
                "nutrition_goals": [],
                "cooking_time_limit": None,
                "difficulty": None,
                "cuisine": "none"
            }
        },
        {
            "name": "场景5: 西餐选项",
            "params": {
                "dietary_preferences": [],
                "food_likes": ["牛排", "西兰花"],
                "food_dislikes": [],
                "health_conditions": [],
                "nutrition_goals": [],
                "cooking_time_limit": 60,
                "difficulty": "medium",
                "cuisine": "western"
            }
        }
    ]
    
    success_count = 0
    total_count = len(test_scenarios)
    
    for scenario in test_scenarios:
        print(f"\n=== {scenario['name']} ===")
        print(f"请求参数: {json.dumps(scenario['params'], ensure_ascii=False, indent=2)}")
        
        try:
            # 模拟CORS预检请求
            options_response = requests.options(
                API_URL,
                headers={
                    "Origin": "http://localhost:5173",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "content-type"
                }
            )
            print(f"OPTIONS请求状态: {options_response.status_code}")
            
            # 发送实际的POST请求
            response = requests.post(
                API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Origin": "http://localhost:5173"
                },
                json=scenario['params']
            )
            
            print(f"POST请求状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 请求成功! 食谱标题: {data.get('title')}")
                success_count += 1
            elif response.status_code == 422:
                try:
                    error_data = response.json()
                    print(f"❌ 422验证错误: {json.dumps(error_data, ensure_ascii=False, indent=2)}")
                except:
                    print(f"❌ 422验证错误: {response.text}")
            else:
                print(f"❌ 请求失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求异常: {str(e)}")
        
        time.sleep(1)  # 添加延迟避免请求过快
    
    print(f"\n=== 测试总结 ===")
    print(f"总测试场景: {total_count}")
    print(f"成功场景: {success_count}")
    print(f"成功率: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 所有测试场景都成功了！API工作正常。")
    else:
        print("⚠️  部分测试场景失败，请检查参数格式。")

if __name__ == "__main__":
    test_frontend_style_requests()