from app.core.database import engine
from sqlalchemy import text

# 检查用户表中是否存在测试用户
try:
    with engine.connect() as conn:
        print('检查用户表中的用户...')
        result = conn.execute(text("""
            SELECT user_id, username, email, is_active, failed_login_attempts, locked_until 
            FROM app_schema.users 
            ORDER BY created_at DESC
        """))
        
        users = result.fetchall()
        if users:
            print(f"找到 {len(users)} 个用户:")
            for user in users:
                print(f"用户ID: {user[0]}, 用户名: {user[1]}, 邮箱: {user[2]}, 激活状态: {user[3]}, 失败尝试: {user[4]}, 锁定时间: {user[5]}")
        else:
            print("用户表中没有用户")
        
        # 检查收藏表结构
        print('\n检查收藏表结构...')
        result = conn.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'favorites' AND table_schema = 'app_schema'
        """))
        
        print('收藏表结构:')
        for row in result:
            print(f"列名: {row[0]}, 数据类型: {row[1]}")
            
        # 检查收藏表中的数据
        print('\n检查收藏表中的数据...')
        result = conn.execute(text("""
            SELECT favorite_id, user_id, recipe_id, created_at 
            FROM app_schema.favorites 
        """))
        
        favorites = result.fetchall()
        if favorites:
            print(f"找到 {len(favorites)} 条收藏记录:")
            for fav in favorites:
                print(f"收藏ID: {fav[0]}, 用户ID: {fav[1]}, 食谱ID: {fav[2]}, 创建时间: {fav[3]}")
        else:
            print("收藏表中没有数据")
            
        # 检查食谱表中的数据
        print('\n检查食谱表中的数据...')
        result = conn.execute(text("""
            SELECT recipe_id, title, created_at 
            FROM app_schema.recipes 
            ORDER BY created_at DESC
            LIMIT 5
        """))
        
        recipes = result.fetchall()
        if recipes:
            print(f"找到 {len(recipes)} 个食谱:")
            for recipe in recipes:
                print(f"食谱ID: {recipe[0]}, 标题: {recipe[1]}, 创建时间: {recipe[2]}")
        else:
            print("食谱表中没有数据")
            
except Exception as e:
    print(f"数据库操作失败: {str(e)}")
