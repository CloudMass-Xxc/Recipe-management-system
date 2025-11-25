import psycopg2
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv(dotenv_path='d:\\Homework\\LLM\\Final_assignment\\Vers_4\\backend\\.env')

# 解析DATABASE_URL
db_url = os.getenv('DATABASE_URL')
# 提取连接信息
# postgresql://app_user:xxc1018@localhost:5432/recipe_system
parts = db_url.split('://')[1].split('@')
user_pass = parts[0].split(':')
host_db = parts[1].split('/')

db_user = user_pass[0]
db_password = user_pass[1]
db_host = host_db[0].split(':')[0]
db_port = host_db[0].split(':')[1]
db_name = host_db[1]

print(f"连接数据库: {db_name} at {db_host}:{db_port} as {db_user}")

try:
    # 连接到PostgreSQL数据库
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    
    # 创建游标
    cur = conn.cursor()
    
    # 查询表结构
    print("\n用户表结构:")
    cur.execute("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'users';")
    columns = cur.fetchall()
    for col in columns:
        print(f"{col[0]}: {col[1]} (Nullable: {col[2]})")
    
    # 查询前5个用户记录，检查phone字段是否有值
    print("\n前5个用户记录的phone字段:")
    cur.execute("SELECT user_id, username, phone FROM users LIMIT 5;")
    users = cur.fetchall()
    if users:
        for user in users:
            print(f"用户ID: {user[0]}, 用户名: {user[1]}, 手机号: {user[2]}")
    else:
        print("没有找到用户记录")
    
    # 关闭游标和连接
    cur.close()
    conn.close()
    
    print("\n数据库查询完成")
    
except Exception as e:
    print(f"数据库连接错误: {e}")
