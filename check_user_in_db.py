import psycopg2
from psycopg2 import OperationalError
import os

# 使用.env文件中的数据库连接信息
db_params = {
    'host': 'localhost',
    'database': 'recipe_system',
    'user': 'app_user',
    'password': 'xxc1018',
    'port': '5432'
}

def connect_to_db():
    try:
        connection = psycopg2.connect(**db_params)
        print("成功连接到数据库")
        return connection
    except OperationalError as e:
        print(f"数据库连接失败: {e}")
        return None

def check_user_table():
    connection = connect_to_db()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        # 首先检查表是否存在
        cursor.execute("""SELECT EXISTS 
                          (SELECT 1 
                           FROM information_schema.tables 
                           WHERE table_name = 'users');""")
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("用户表 'users' 存在")
            
            # 查看表结构
            print("\n用户表结构:")
            cursor.execute("""SELECT column_name, data_type 
                              FROM information_schema.columns 
                              WHERE table_name = 'users';""")
            columns = cursor.fetchall()
            for column in columns:
                print(f"  {column[0]}: {column[1]}")
            
            # 查询手机号为13160697108的用户
            print("\n查询手机号为13160697108的用户:")
            cursor.execute("""SELECT user_id, phone, username, email, is_active, created_at 
                              FROM users 
                              WHERE phone = '13160697108';""")
            user = cursor.fetchone()
            
            if user:
                print(f"用户存在: {user}")
                
                # 验证密码哈希是否存在
                cursor.execute("""SELECT password_hash 
                                  FROM users 
                                  WHERE phone = '13160697108';""")
                password_hash = cursor.fetchone()
                print(f"密码哈希: {password_hash}")
            else:
                print("未找到手机号为13160697108的用户")
            
            # 查询所有用户的基本信息
            print("\n所有用户的基本信息:")
            cursor.execute("""SELECT user_id, phone, username, is_active 
                              FROM users 
                              LIMIT 10;""")
            users = cursor.fetchall()
            
            if users:
                for user in users:
                    print(f"  {user}")
            else:
                print("用户表为空")
        else:
            print("用户表 'users' 不存在")
            
    except Exception as e:
        print(f"查询数据库时出错: {e}")
    finally:
        if connection:
            connection.close()
            print("\n数据库连接已关闭")

if __name__ == "__main__":
    check_user_table()