from app.core.database import get_db
from app.ai_service.schemas import SaveRecipeRequest, RecipeResponse, Ingredient, NutritionInfo, Difficulty
from app.recipes.services import RecipeService
from app.models.user import User
import json

# 测试API路由处理过程
def test_api_route_process():
    print("正在测试API路由处理过程...")
    
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
        
        # 1. 模拟前端发送的原始数据
        print("\n1. 模拟前端发送的原始数据:")
        frontend_data = {
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
        print(json.dumps(frontend_data, ensure_ascii=False, indent=2))
        
        # 2. 模拟前端调用API的请求体
        print("\n2. 模拟前端调用API的请求体:")
        request_body = {
            "recipe_data": frontend_data,
            "share_with_community": False
        }
        print(json.dumps(request_body, ensure_ascii=False, indent=2))
        
        # 3. 模拟API路由中的数据模型转换（这是可能出现问题的地方）
        print("\n3. 模拟API路由中的数据模型转换:")
        try:
            # 将原始数据转换为RecipeResponse模型
            recipe_response = RecipeResponse(**frontend_data)
            print(f"RecipeResponse模型转换成功")
            
            # 将RecipeResponse模型和share_with_community标志转换为SaveRecipeRequest模型
            save_request = SaveRecipeRequest(
                recipe_data=recipe_response,
                share_with_community=False
            )
            print(f"SaveRecipeRequest模型转换成功")
            
            # 4. 模拟API路由中的数据处理
            print("\n4. 模拟API路由中的数据处理:")
            # 从SaveRecipeRequest中提取recipe_data并转换为字典
            recipe_data = save_request.recipe_data.model_dump()
            
            # 模拟API路由中的数据处理逻辑
            if isinstance(recipe_data.get("instructions"), list):
                recipe_data["instructions"] = "\n".join(recipe_data["instructions"])
            
            if "tips" in recipe_data and isinstance(recipe_data["tips"], list):
                recipe_data["tips"] = "\n".join(recipe_data["tips"])
            
            recipe_data.pop("tips", None)
            recipe_data.pop("prep_time", None)
            
            print("处理后的数据:")
            print(json.dumps(recipe_data, ensure_ascii=False, indent=2))
            
            # 5. 调用RecipeService.create_recipe保存食谱
            print("\n5. 调用RecipeService.create_recipe保存食谱...")
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
            print(f"\n错误: 数据模型转换过程中发生异常")
            print(f"异常类型: {type(e).__name__}")
            print(f"异常信息: {str(e)}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"\n错误: 测试过程中发生异常")
        print(f"异常类型: {type(e).__name__}")
        print(f"异常信息: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭数据库会话
        db.close()

# 运行测试
if __name__ == "__main__":
    test_api_route_process()
