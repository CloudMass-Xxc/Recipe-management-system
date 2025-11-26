from app.core.database import engine
from sqlalchemy import text
import requests
import json

# 使用数据库中已存在的用户进行测试
def test_favorite_functionality():
    try:
        # 首先检查数据库中是否有用户和食谱
        with engine.connect() as conn:
            print("正在检查数据库...")
            
            # 获取第一个用户
            user_result = conn.execute(text("""
                SELECT user_id, username, email 
                FROM app_schema.users 
                ORDER BY created_at DESC 
                LIMIT 1
            """))
            user = user_result.fetchone()
            
            if not user:
                print("❌ 数据库中没有用户")
                return
            
            print(f"找到用户: {user[1]} ({user[2]})")
            
            # 获取第一个食谱
            recipe_result = conn.execute(text("""
                SELECT recipe_id, title 
                FROM app_schema.recipes 
                ORDER BY created_at DESC 
                LIMIT 1
            """))
            recipe = recipe_result.fetchone()
            
            if not recipe:
                print("❌ 数据库中没有食谱")
                return
            
            print(f"找到食谱: {recipe[1]} ({recipe[0]})")
            
            # 测试用户已存在，直接登录
            print("\n测试用户已存在，直接登录: test_favorite_user")
            test_user_data = {
                "username": "test_favorite_user",
                "email": "test_favorite@example.com",
                "password": "Test123456"
            }
            login_data = {
                "identifier": test_user_data["email"],
                "password": test_user_data["password"]
            }
            
            # 登录获取token
            print("\n正在登录...")
            login_response = requests.post(
                "http://localhost:8001/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if login_response.status_code != 200:
                print(f"❌ 登录失败: {login_response.status_code} - {login_response.text}")
                return
            
            login_result = login_response.json()
            token = login_result["access_token"]
            print(f"✅ 登录成功，获取到令牌")
            
            # 设置请求头
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            recipe_id = str(recipe[0])
            
            # 1. 先尝试取消收藏（如果已经收藏）
            print(f"\n步骤1: 尝试取消收藏食谱: {recipe[1]} ({recipe_id})...")
            unfavorite_response = requests.delete(
                f"http://localhost:8001/recipes/{recipe_id}/favorite",
                headers=headers
            )
            
            if unfavorite_response.status_code == 204:
                print(f"✅ 取消收藏成功! 状态码: {unfavorite_response.status_code}")
            else:
                print(f"ℹ️  取消收藏状态: {unfavorite_response.status_code} - {unfavorite_response.text}")
            
            # 2. 测试添加收藏
            print(f"\n步骤2: 测试添加收藏食谱: {recipe[1]} ({recipe_id})...")
            add_response = requests.post(
                f"http://localhost:8001/recipes/{recipe_id}/favorite",
                headers=headers
            )
            
            if add_response.status_code == 200:
                print(f"✅ 添加收藏成功! 状态码: {add_response.status_code}")
                print(f"响应内容: {add_response.text}")
            else:
                print(f"❌ 添加收藏失败: {add_response.status_code} - {add_response.text}")
                return
            
            # 3. 再次测试取消收藏
            print(f"\n步骤3: 测试取消收藏食谱: {recipe[1]} ({recipe_id})...")
            remove_response = requests.delete(
                f"http://localhost:8001/recipes/{recipe_id}/favorite",
                headers=headers
            )
            
            if remove_response.status_code == 204:
                print(f"✅ 取消收藏成功! 状态码: {remove_response.status_code}")
            else:
                print(f"❌ 取消收藏失败: {remove_response.status_code} - {remove_response.text}")
                return
            
            # 4. 最后再次添加收藏（恢复状态）
            print(f"\n步骤4: 最后添加收藏（恢复状态）: {recipe[1]} ({recipe_id})...")
            final_add_response = requests.post(
                f"http://localhost:8001/recipes/{recipe_id}/favorite",
                headers=headers
            )
            
            if final_add_response.status_code == 200:
                print(f"✅ 最终添加收藏成功! 状态码: {final_add_response.status_code}")
            else:
                print(f"❌ 最终添加收藏失败: {final_add_response.status_code} - {final_add_response.text}")
                return
            
            print("\n🎉 测试完成！收藏功能正常工作！")
            
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_favorite_functionality()
