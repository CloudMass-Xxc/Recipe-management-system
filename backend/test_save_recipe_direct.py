from app.core.database import get_db
from app.recipes.services import RecipeService
from app.models.user import User
from sqlalchemy.orm import Session
import json

# 模拟用户对象
class MockUser:
    def __init__(self, user_id):
        self.user_id = user_id

# 测试直接调用RecipeService保存食谱
def test_save_recipe_direct():
    print("正在测试直接调用RecipeService保存食谱...")
    
    # 获取数据库会话
    db = next(get_db())
    
    try:
        # 获取一个真实的用户ID
        user = db.query(User).first()
        if not user:
            print("数据库中没有用户，请先创建用户")
            return
        
        user_id = user.user_id
        print(f"使用用户ID: {user_id}")
        
        # 准备食谱数据，模拟前端发送的数据结构
        recipe_data = {
            "title": "测试食谱",
            "description": "这是一个测试用的食谱",
            "difficulty": "easy",
            "cooking_time": 30,
            "prep_time": 10,
            "servings": 2,
            "instructions": "准备食材\n烹饪\n享用",  # 字符串格式，与前端处理后的格式一致
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
        
        print("食谱数据:")
        print(json.dumps(recipe_data, ensure_ascii=False, indent=2))
        
        # 调用RecipeService.create_recipe方法
        print("\n调用RecipeService.create_recipe保存食谱...")
        new_recipe = RecipeService.create_recipe(db, user_id, recipe_data)
        
        if new_recipe:
            print("\n食谱保存成功！")
            print(f"食谱ID: {new_recipe.recipe_id}")
            print(f"标题: {new_recipe.title}")
            print(f"描述: {new_recipe.description}")
            print(f"烹饪时间: {new_recipe.cooking_time}")
            print(f"份量: {new_recipe.servings}")
            print(f"食材数量: {len(new_recipe.ingredients) if new_recipe.ingredients else 0}")
            
            # 检查营养信息
            if new_recipe.nutrition_info:
                print("\n营养信息:")
                print(f"卡路里: {new_recipe.nutrition_info.calories}")
                print(f"蛋白质: {new_recipe.nutrition_info.protein}")
                print(f"碳水化合物: {new_recipe.nutrition_info.carbs}")
                print(f"脂肪: {new_recipe.nutrition_info.fat}")
                print(f"膳食纤维: {new_recipe.nutrition_info.fiber}")
            else:
                print("\n警告: 没有找到营养信息")
        else:
            print("\n错误: 保存食谱失败，RecipeService.create_recipe返回None")
            
    except Exception as e:
        print(f"\n错误: 保存食谱时发生异常")
        print(f"异常类型: {type(e).__name__}")
        print(f"异常信息: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭数据库会话
        db.close()

# 运行测试
if __name__ == "__main__":
    test_save_recipe_direct()
