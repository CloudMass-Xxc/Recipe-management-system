import requests
import json
import time

# 测试AI生成食谱API，验证菜系参数
print("开始测试AI生成食谱功能 - 菜系参数")
print("=" * 50)

# 测试数据 - 中餐
chinese_test_data = {
    "dietary_preferences": [],
    "food_likes": ["鸡肉", "青菜", "米饭"],
    "food_dislikes": [],
    "health_conditions": [],
    "nutrition_goals": [],
    "cooking_time_limit": 30,
    "difficulty": "easy",
    "cuisine": "chinese"
}

# 测试数据 - 西餐
western_test_data = {
    "dietary_preferences": [],
    "food_likes": ["beef", "potato", "cheese"],
    "food_dislikes": [],
    "health_conditions": [],
    "nutrition_goals": [],
    "cooking_time_limit": 45,
    "difficulty": "medium",
    "cuisine": "western"
}

def test_recipe_generation(data, cuisine_name):
    """测试指定菜系的食谱生成"""
    print(f"\n测试生成{ cuisine_name }食谱...")
    print(f"请求参数: {json.dumps(data, ensure_ascii=False)}")
    
    try:
        # 注意：实际环境中需要获取有效的token
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer test_token"  # 这里需要替换为实际的token
        }
        
        # 发送请求到AI生成食谱端点
        response = requests.post(
            "http://localhost:8000/ai/generate-recipe",
            headers=headers,
            json=data,
            timeout=60  # 设置较长的超时时间，因为AI生成可能需要时间
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            recipe = response.json()
            print(f"成功生成{ cuisine_name }食谱:")
            print(f"  标题: {recipe.get('title')}")
            print(f"  描述: {recipe.get('description')}")
            print(f"  烹饪时间: {recipe.get('cooking_time')}分钟")
            print(f"  难度: {recipe.get('difficulty')}")
            print(f"  食材数量: {len(recipe.get('ingredients', []))}种")
            print(f"  步骤数量: {len(recipe.get('instructions', []))}步")
            return True
        else:
            print(f"错误: {response.text}")
            return False
    except Exception as e:
        print(f"请求异常: {str(e)}")
        return False

# 执行测试
print("注意：这个测试需要有效的认证token才能成功。")
print("如果遇到401错误，请替换脚本中的Authorization token。")
print("\n测试结果仅供参考，主要验证API是否接受cuisine参数...")
print("=" * 50)

# 测试中餐生成
test_recipe_generation(chinese_test_data, "中餐")
print("\n等待5秒后测试西餐生成...")
time.sleep(5)

# 测试西餐生成
test_recipe_generation(western_test_data, "西餐")

print("\n" + "=" * 50)
print("测试完成！如果API接受cuisine参数，则菜系选择功能已修复。")
print("提示：在前端使用时，请确保用户已登录并有有效的token。")