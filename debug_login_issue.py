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
    
    # 1. 检查测试用户的完整信息
    target_phone = "13160697108"
    print(f"详细检查手机号为 {target_phone} 的用户信息：")
    
    cur.execute("""
    SELECT user_id, username, phone, email, password_hash, is_active, 
           created_at, updated_at 
    FROM users 
    WHERE phone = %s;
    """, (target_phone,))
    
    user = cur.fetchone()
    if user:
        print(f"✓ 找到用户记录：")
        print(f"  用户ID: {user[0]}")
        print(f"  用户名: {user[1]}")
        print(f"  手机号: {user[2]}")
        print(f"  邮箱: {user[3]}")
        print(f"  密码哈希: {user[4][:30]}...")
        print(f"  is_active: '{user[5]}' (类型: {type(user[5]).__name__})")
        print(f"  创建时间: {user[6]}")
        
        # 确保is_active是'Y'
        if user[5] != 'Y':
            print(f"⚠️  is_active不是'Y'，更新中...")
            cur.execute(
                "UPDATE users SET is_active = 'Y' WHERE phone = %s;",
                (target_phone,)
            )
            print(f"✓ 已将is_active更新为'Y'")
        else:
            print(f"✓ is_active状态正确")
    else:
        print(f"❌ 未找到手机号为 {target_phone} 的用户")
    
    # 2. 检查数据库中是否有索引
    print("\n检查索引情况：")
    cur.execute("""
    SELECT indexname 
    FROM pg_indexes 
    WHERE tablename = 'users' AND indexdef LIKE '%phone%';
    """)
    indexes = cur.fetchall()
    if indexes:
        print(f"✓ 找到{len(indexes)}个与phone相关的索引：")
        for idx in indexes:
            print(f"  - {idx[0]}")
    else:
        print("! 未找到与phone相关的索引")
    
    # 3. 直接使用SQL查询验证手机号是否能正确查询
    print("\n直接使用SQL查询验证：")
    cur.execute(
        "SELECT COUNT(*) FROM users WHERE phone = %s;",
        (target_phone,)
    )
    count = cur.fetchone()[0]
    print(f"使用手机号 '{target_phone}' 查询结果：{count} 条记录")
    
    # 关闭连接
    cur.close()
    conn.close()
    
    print("\n调试完成！")
    
except Exception as e:
    print(f"数据库操作错误: {e}")
