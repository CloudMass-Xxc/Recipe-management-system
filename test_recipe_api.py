import requests
import json

# 测试获取食谱详情
def test_get_recipe_detail():
    # 使用一个已知存在的食谱ID
    recipe_id = "b3afa3fb-007b-4dd8-8c09-12ebb6ab9ed9"
    url = f"http://localhost:8001/recipes/{recipe_id}"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            recipe_data = response.json()
            print("Recipe Detail:")
            print(json.dumps(recipe_data, indent=2, ensure_ascii=False))
            
            # 检查是否包含所有必要字段
            required_fields = ["recipe_id", "title", "description", "instructions", "cooking_time", "servings", "difficulty", "ingredients", "tags", "image_url", "nutrition_info", "author_id", "author_name", "created_at", "updated_at"]
            for field in required_fields:
                if field in recipe_data:
                    print(f"✓ {field} is present")
                else:
                    print(f"✗ {field} is missing")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_get_recipe_detail()
