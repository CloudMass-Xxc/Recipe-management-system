import psycopg2
import os
from psycopg2 import OperationalError

def clear_user_data():
    print("开始清空用户数据操作...")
    
    # 数据库连接信息
    db_params = {
        'host': 'localhost',
        'database': 'recipe_system',
        'user': 'app_user',
        'password': 'xxc1018',  # 用户提供的正确密码
        'port': '5432'
    }
    
    connection = None
    cursor = None
    
    try:
        # 连接到数据库
        print("正在连接数据库...")
        connection = psycopg2.connect(**db_params)
        connection.autocommit = True
        cursor = connection.cursor()
        
        # 检查数据库状态
        print("数据库连接成功！")
        cursor.execute("SELECT version();")
        print(f"数据库版本: {cursor.fetchone()[0]}")
        
        # 检查用户表是否存在
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE  table_schema = 'public' 
                AND    table_name   = 'users'
            );
        """)
        
        if cursor.fetchone()[0]:
            print("检测到users表存在")
            
            # 检查用户表中的记录数
            cursor.execute("SELECT COUNT(*) FROM users;")
            user_count = cursor.fetchone()[0]
            print(f"当前用户表中有 {user_count} 条记录")
            
            if user_count > 0:
                # 显示前5条用户数据
                print("\n前5条用户数据:")
                cursor.execute("SELECT user_id, username, email FROM users LIMIT 5;")
                users = cursor.fetchall()
                for user in users:
                    print(f"用户ID: {user[0]}, 用户名: {user[1]}, 邮箱: {user[2]}")
                
                # 尝试清空用户数据
                print("\n尝试清空用户数据...")
                
                # 使用TRUNCATE CASCADE命令
                try:
                    cursor.execute("TRUNCATE TABLE users CASCADE;")
                    print("TRUNCATE命令执行成功！")
                except Exception as e:
                    print(f"TRUNCATE命令执行失败: {e}")
                    print("尝试使用DELETE命令...")
                    # 尝试使用DELETE命令
                    cursor.execute("DELETE FROM users;")
                    print("DELETE命令执行成功！")
                
                # 验证数据是否已清空
                cursor.execute("SELECT COUNT(*) FROM users;")
                remaining_count = cursor.fetchone()[0]
                print(f"\n清空后用户表中有 {remaining_count} 条记录")
                
                if remaining_count == 0:
                    print("✅ 成功清空用户数据！")
                else:
                    print("❌ 未能完全清空用户数据")
            else:
                print("用户表已经是空的")
        else:
            print("错误: 未找到users表")
            
    except OperationalError as e:
        print(f"数据库操作错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("数据库连接已关闭")

if __name__ == "__main__":
    clear_user_data()
