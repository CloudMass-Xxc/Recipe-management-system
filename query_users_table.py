import psycopg2
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接信息 - 使用正确的密码（从check_user_in_db.py获取）
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "recipe_system"
DB_USER = "app_user"
DB_PASSWORD = "xxc1018"

def query_users_table():
    """
    查询用户表中的所有数据
    """
    try:
        # 连接数据库
        print(f"正在连接数据库: host={DB_HOST}, port={DB_PORT}, dbname={DB_NAME}, user={DB_USER}")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("数据库连接成功")
        
        # 创建游标
        cursor = conn.cursor()
        
        # 查询用户表结构
        print("\n查询用户表结构:")
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users'")
        columns = cursor.fetchall()
        print("列名 | 数据类型")
        print("--- | ---")
        for column in columns:
            print(f"{column[0]} | {column[1]}")
        
        # 查询用户表所有数据
        print("\n查询用户表所有数据:")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        if users:
            print(f"\n找到 {len(users)} 个用户记录:")
            # 获取列名
            column_names = [desc[0] for desc in cursor.description]
            
            # 打印表头
            print("\n用户数据:")
            print("=" * 80)
            for i, column_name in enumerate(column_names):
                print(f"{column_name:<20}", end="")
                if (i + 1) % 3 == 0:  # 每3列换一行，避免输出太长
                    print()
            print()
            print("=" * 80)
            
            # 打印用户数据
            for i, user in enumerate(users):
                print(f"记录 {i+1}:")
                for j, value in enumerate(user):
                    # 对于长文本（如密码哈希）只显示部分
                    display_value = value
                    if isinstance(value, str) and len(value) > 30:
                        display_value = value[:30] + "..."
                    print(f"  {column_names[j]:<20}: {display_value}")
                print("-" * 80)
        else:
            print("用户表中没有数据")
        
    except Exception as e:
        print(f"查询数据库时出错: {str(e)}")
    finally:
        # 关闭连接
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print("数据库连接已关闭")

if __name__ == "__main__":
    print("开始查询用户表数据...")
    query_users_table()
    print("查询完成!")