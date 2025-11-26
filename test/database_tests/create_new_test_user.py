import psycopg2
import sys

# 确保使用正确的Python路径来导入后端的密码处理函数
sys.path.append('d:\\Homework\\LLM\\Final_assignment\\Vers_4\\backend')

try:
    # 直接从后端导入密码处理函数，确保完全一致
    from app.auth.password import get_password_hash, generate_user_id
    print("✓ 成功导入后端密码处理函数")
except Exception as e:
    print(f"! 导入后端函数失败，使用本地实现: {e}")
    # 本地实现（与后端完全相同）
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
    
    def get_password_hash(password: str) -> str:
        password = password[:72]
        return pwd_context.hash(password)
    
    def generate_user_id() -> str:
        import uuid
        return str(uuid.uuid4())

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
    
    # 测试用户信息
    test_phone = "13160697108"
    test_password = "password123"
    test_username = "test_user_fixed"
    test_email = "test_user_fixed@example.com"
    
    # 生成用户ID和密码哈希
    user_id = generate_user_id()
    hashed_password = get_password_hash(test_password)
    
    print(f"生成的用户信息：")
    print(f"  用户ID: {user_id}")
    print(f"  手机号: {test_phone}")
    print(f"  密码: {test_password}")
    print(f"  密码哈希: {hashed_password}")
    
    # 先删除可能存在的同名用户
    cur.execute("DELETE FROM users WHERE phone = %s;", (test_phone,))
    print(f"✓ 已清理可能存在的同名用户")
    
    # 插入新的测试用户
    cur.execute("""
    INSERT INTO users (user_id, username, email, phone, password_hash, is_active, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, 'Y', NOW(), NOW())
    RETURNING user_id;
    """, 
    (user_id, test_username, test_email, test_phone, hashed_password))
    
    new_user_id = cur.fetchone()[0]
    print(f"\n✓ 成功创建新的测试用户！")
    print(f"  用户ID: {new_user_id}")
    print(f"  用户名: {test_username}")
    print(f"  手机号: {test_phone}")
    print(f"  密码: {test_password}")
    print(f"  密码哈希已使用后端相同的算法生成")
    
    # 验证用户是否创建成功
    cur.execute(
        "SELECT user_id, username, phone, is_active FROM users WHERE phone = %s;",
        (test_phone,)
    )
    user = cur.fetchone()
    if user:
        print(f"\n验证成功：")
        print(f"  用户ID: {user[0]}")
        print(f"  用户名: {user[1]}")
        print(f"  手机号: {user[2]}")
        print(f"  is_active: '{user[3]}'")
    
    # 关闭连接
    cur.close()
    conn.close()
    
    print("\n操作完成！请尝试使用此测试用户登录。")
    
except Exception as e:
    print(f"数据库操作错误: {e}")
