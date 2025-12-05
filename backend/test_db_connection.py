import psycopg2

try:
    # 尝试连接数据库
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="recipe_system",
        user="app_user",
        password="xxc1018"
    )
    print("数据库连接成功!")
    
    # 尝试执行一个简单的查询
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        result = cur.fetchone()
        print(f"查询结果: {result}")
    
    # 检查app_schema是否存在
    with conn.cursor() as cur:
        cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'app_schema'")
        if cur.fetchone():
            print("app_schema已存在")
        else:
            print("app_schema不存在，尝试创建...")
            cur.execute("CREATE SCHEMA IF NOT EXISTS app_schema")
            conn.commit()
            print("app_schema创建成功")
    
    # 检查users表是否存在
    with conn.cursor() as cur:
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'app_schema' AND table_name = 'users'")
        if cur.fetchone():
            print("users表已存在")
        else:
            print("users表不存在")
    
    conn.close()
except Exception as e:
    print(f"数据库连接失败: {e}")
