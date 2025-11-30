import requests
import json

# 1. 获取食谱列表，查看有效的食谱ID
print("=== 获取食谱列表 ===")
try:
    recipes_response = requests.get('http://localhost:8002/recipes/')
    print(f"Status Code: {recipes_response.status_code}")
    
    # 检查响应内容
    print("响应原始内容前100字符:", recipes_response.text[:100])
    
    response_data = recipes_response.json()
    recipes = response_data.get('recipes', [])
    print(f"食谱数量: {len(recipes)}")
    
    if len(recipes) > 0:
        print("第一个食谱:")
        first_recipe = recipes[0]
        print(f"ID: {first_recipe.get('recipe_id')}")
        print(f"Title: {first_recipe.get('title')}")
        print(f"Instructions类型: {type(first_recipe.get('instructions'))}")
        print(f"Instructions内容: {first_recipe.get('instructions')}")
        
        # 2. 使用第一个食谱的ID测试详情API
        recipe_id = first_recipe['recipe_id']
        print(f"\n=== 测试食谱详情 (ID: {recipe_id}) ===")
        
        detail_response = requests.get(f'http://localhost:8002/recipes/{recipe_id}/')
        print(f"Status Code: {detail_response.status_code}")
        
        detail = detail_response.json()
        print("详情API返回的instructions:")
        print(f"类型: {type(detail.get('instructions'))}")
        print(f"内容: {detail.get('instructions')}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
