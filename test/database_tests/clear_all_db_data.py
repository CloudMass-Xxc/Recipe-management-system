import psycopg2
import os

def clear_all_database_data():
    print("开始清空数据库所有数据...")
    
    # 数据库连接信息
    db_params = {
        'host': 'localhost',
        'database': 'recipe_system',
        'user': 'app_user',
        'password': 'xxc1018',
        'port': '5432'
    }
    
    connection = None
    cursor = None
    
    # 按照外键依赖顺序清空表
    # 先清空依赖其他表的表
    tables_to_clear = [
        'app_schema.user_recipe_interactions',
        'app_schema.diet_plans',
        'app_schema.recipe_ingredients',
        'app_schema.ingredients',
        'app_schema.recipes',
        'app_schema.users'
    ]
    
    try:
        # 连接到数据库
        print("正在连接数据库...")
        connection = psycopg2.connect(**db_params)
        connection.autocommit = True
        cursor = connection.cursor()
        
        print("数据库连接成功！")
        
        # 先检查每个表的记录数
        print("\n清空前的记录数：")
        for table in tables_to_clear:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                print(f"{table}: {count} 条记录")
            except Exception as e:
                print(f"无法获取 {table} 的记录数: {e}")
        
        # 清空所有表数据
        print("\n开始清空数据...")
        for table in tables_to_clear:
            print(f"清空表 {table}...")
            try:
                # 尝试使用TRUNCATE CASCADE
                cursor.execute(f"TRUNCATE TABLE {table} CASCADE;")
                print(f"  ✅ {table} 清空成功")
            except Exception as e:
                print(f"  ❌ TRUNCATE失败: {e}")
                try:
                    # 如果TRUNCATE失败，尝试使用DELETE
                    cursor.execute(f"DELETE FROM {table};")
                    print(f"  ✅ DELETE成功")
                except Exception as delete_error:
                    print(f"  ❌ DELETE也失败: {delete_error}")
        
        # 验证清空结果
        print("\n清空后的记录数：")
        all_cleared = True
        for table in tables_to_clear:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                status = "✅ 已清空" if count == 0 else f"❌ 未清空（{count}条）"
                print(f"{table}: {count} 条记录 {status}")
                if count > 0:
                    all_cleared = False
            except Exception as e:
                print(f"无法验证 {table}: {e}")
        
        # 总结
        if all_cleared:
            print("\n🎉 所有表数据已成功清空！")
        else:
            print("\n⚠️  部分表未能清空，请检查")
    
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭连接
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("数据库连接已关闭")

if __name__ == "__main__":
    clear_all_database_data()
