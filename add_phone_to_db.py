import psycopg2
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv(dotenv_path='d:\\Homework\\LLM\\Final_assignment\\Vers_4\\backend\\.env')

# 使用postgres超级用户连接（用于修改表结构）
db_user = "postgres"
db_password = "xxc1018"  # 使用与app_user相同的密码
db_host = "localhost"
db_port = "5432"
db_name = "recipe_system"

try:
    # 连接到PostgreSQL数据库
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    conn.autocommit = True  # 设置自动提交
    
    # 创建游标
    cur = conn.cursor()
    
    # 执行SQL命令添加phone字段
    print("开始添加phone字段...")
    
    # 1. 添加phone字段
    try:
        cur.execute("ALTER TABLE users ADD COLUMN phone VARCHAR(20) UNIQUE;")
        print("✓ 成功添加phone字段")
    except psycopg2.errors.DuplicateColumn:
        print("✓ phone字段已存在")
    
    # 2. 创建索引 (可选，因为表结构已经创建好了)
    print("✓ 索引检查跳过，专注于添加手机号数据")
    # 注释掉索引创建，因为它已经存在
    
    # 3. 给现有用户添加示例手机号数据
    try:
        # 先获取所有用户ID
        cur.execute("SELECT user_id FROM users WHERE phone IS NULL ORDER BY user_id;")
        users_to_update = cur.fetchall()
        
        # 为每个用户分配一个唯一的手机号
        for i, (user_id,) in enumerate(users_to_update, 1):
            phone = f"1380000000{i}"  # 简单的手机号生成逻辑
            cur.execute("UPDATE users SET phone = %s WHERE user_id = %s;", (phone, user_id))
        
        print(f"✓ 已为{len(users_to_update)}个用户添加了手机号")
    except Exception as e:
        print(f"! 更新用户手机号时出错: {e}")
    
    # 4. 验证字段添加成功
    print("\n验证表结构:")
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'phone';")
    result = cur.fetchone()
    if result:
        print("✓ phone字段已成功添加到数据库表")
    else:
        print("! phone字段添加失败")
    
    # 5. 显示部分用户数据
    print("\n前5个用户的phone字段数据:")
    cur.execute("SELECT user_id, username, phone FROM users LIMIT 5;")
    users = cur.fetchall()
    for user in users:
        print(f"用户ID: {user[0]}, 用户名: {user[1]}, 手机号: {user[2]}")
    
    # 关闭连接
    cur.close()
    conn.close()
    
    print("\n操作完成！")
    
except Exception as e:
    print(f"数据库操作错误: {e}")
