import requests
import json
import time
import sys

# 后端API地址
API_URL = "http://localhost:8000/ai/generate-recipe"

def test_recipe_generation(params, test_name):
    """测试食谱生成API，打印详细的错误信息"""
    print(f"\n=== 测试: {test_name} ===")
    print(f"请求参数: {json.dumps(params, ensure_ascii=False, indent=2)}")
    
    try:
        # 发送请求
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            json=params
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应成功! 食谱标题: {data.get('title')}")
            return True
        elif response.status_code == 422:
            # 422错误通常包含详细的验证错误信息
            try:
                error_data = response.json()
                print(f"422错误详情: {json.dumps(error_data, ensure_ascii=False, indent=2)}")
            except:
                print(f"无法解析422错误详情: {response.text}")
            return False
        else:
            print(f"请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"请求异常: {str(e)}")
        return False

def run_comprehensive_tests():
    """运行全面的测试用例"""
    # 测试用例1: 基本参数 - 应该正常工作
    test1_params = {
        "dietary_preferences": [],
        "food_likes": ["西红柿", "鸡蛋"],
        "food_dislikes": [],
        "health_conditions": [],
        "nutrition_goals": [],
        "cooking_time_limit": 30,
        "difficulty": "easy",
        "cuisine": "chinese"
    }
    test_recipe_generation(test1_params, "基本参数")
    time.sleep(2)  # 添加延迟避免请求过快
    
    # 测试用例2: 空值测试
    test2_params = {
        "dietary_preferences": [],
        "food_likes": [],
        "food_dislikes": [],
        "health_conditions": [],
        "nutrition_goals": [],
        "cooking_time_limit": None,
        "difficulty": None,
        "cuisine": "none"
    }
    test_recipe_generation(test2_params, "空值测试")
    time.sleep(2)
    
    # 测试用例3: 复杂参数
    test3_params = {
        "dietary_preferences": ["vegetarian"],
        "food_likes": ["西兰花", "豆腐", "胡萝卜"],
        "food_dislikes": ["洋葱"],
        "health_conditions": [],
        "nutrition_goals": ["高纤维"],
        "cooking_time_limit": 45,
        "difficulty": "medium",
        "cuisine": "chinese"
    }
    test_recipe_generation(test3_params, "复杂参数")
    time.sleep(2)
    
    # 测试用例4: 无效难度值
    test4_params = {
        "dietary_preferences": [],
        "food_likes": ["鸡肉"],
        "food_dislikes": [],
        "health_conditions": [],
        "nutrition_goals": [],
        "cooking_time_limit": 30,
        "difficulty": "invalid_value",  # 无效值
        "cuisine": "chinese"
    }
    test_recipe_generation(test4_params, "无效难度值")
    time.sleep(2)
    
    # 测试用例5: 无效菜系值
    test5_params = {
        "dietary_preferences": [],
        "food_likes": ["牛肉"],
        "food_dislikes": [],
        "health_conditions": [],
        "nutrition_goals": [],
        "cooking_time_limit": 30,
        "difficulty": "easy",
        "cuisine": "invalid_cuisine"  # 无效值
    }
    test_recipe_generation(test5_params, "无效菜系值")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    print("开始测试食谱生成API...")
    run_comprehensive_tests()