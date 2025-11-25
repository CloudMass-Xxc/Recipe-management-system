import psycopg2

# 数据库连接参数
db_user = "postgres"
db_password = "xxc1018"
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
    conn.autocommit = True
    cur = conn.cursor()
    
    # 1. 检查当前用户表中的phone字段情况
    print("检查当前用户数据:")
    cur.execute("SELECT user_id, username, phone FROM users LIMIT 10;")
    users = cur.fetchall()
    
    if not users:
        print("警告: 用户表中没有找到用户记录")
    else:
        print(f"找到{len(users)}个用户记录")
        for user in users:
            print(f"用户ID: {user[0]}, 用户名: {user[1]}, 手机号: {user[2] or 'NULL'}")
    
    # 2. 检查是否有手机号为13160697108的用户（用户正在尝试使用的手机号）
    print("\n检查用户正在使用的手机号...")
    target_phone = "13160697108"
    cur.execute("SELECT user_id, username FROM users WHERE phone = %s;", (target_phone,))
    user_with_phone = cur.fetchone()
    
    if user_with_phone:
        print(f"✓ 手机号 {target_phone} 已存在，属于用户: {user_with_phone[1]}")
    else:
        print(f"! 手机号 {target_phone} 不存在，需要添加")
        # 3. 添加一个测试用户，使用用户正在尝试登录的手机号
        try:
            # 先检查是否有可用的用户名
            cur.execute("SELECT COUNT(*) FROM users WHERE username = 'test_user';")
            count = cur.fetchone()[0]
            username = f"test_user_{count + 1}" if count > 0 else "test_user"
            
            # 插入测试用户（使用与原系统兼容的字段）
            cur.execute("""
            INSERT INTO users (username, password_hash, email, phone, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, 'Y', NOW(), NOW())
            RETURNING user_id;
            """, 
            (username, 
             '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  # 密码: password123
             f"{username}@example.com",
             target_phone))
            
            new_user_id = cur.fetchone()[0]
            print(f"✓ 成功添加测试用户: {username}, 用户ID: {new_user_id}, 手机号: {target_phone}")
            print("  登录密码: password123")
        except Exception as e:
            print(f"! 添加测试用户失败: {e}")
    
    # 关闭连接
    cur.close()
    conn.close()
    print("\n操作完成！")
    
except Exception as e:
    print(f"数据库操作错误: {e}")
