import psycopg2
import os
import uuid
from passlib.context import CryptContext
from dotenv import load_dotenv

# 密码加密上下文
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# 生成密码哈希
def get_password_hash(password):
    return pwd_context.hash(password)

# 生成用户ID
def generate_user_id():
    return str(uuid.uuid4())

# 直接设置数据库连接信息（避免环境变量加载问题）
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'recipe_system'
DB_USER = 'app_user'
DB_PASSWORD = 'xxc1018'

# 测试用户信息
TEST_PHONE = '13160697108'
TEST_PASSWORD = 'password123'
TEST_USERNAME = 'test_user_fixed'

print(f"开始清理并重新创建测试用户...")
print(f"测试手机号: {TEST_PHONE}")
print(f"测试密码: {TEST_PASSWORD}")

# 连接数据库
conn = None
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    print("成功连接到数据库")
    
    # 查询当前手机号对应的所有用户
    print(f"查询手机号 {TEST_PHONE} 对应的所有用户...")
    cursor.execute("SELECT user_id, username, is_active FROM users WHERE phone = %s", (TEST_PHONE,))
    users = cursor.fetchall()
    
    if users:
        print(f"找到 {len(users)} 个用户使用该手机号:")
        for user in users:
            print(f"  - 用户ID: {user[0]}, 用户名: {user[1]}, 状态: {user[2]}")
        
        # 删除所有使用该手机号的用户
        print("删除所有使用该手机号的用户...")
        cursor.execute("DELETE FROM users WHERE phone = %s", (TEST_PHONE,))
        conn.commit()
        print(f"已删除 {cursor.rowcount} 个用户")
    else:
        print("未找到使用该手机号的用户")
    
    # 生成密码哈希
    password_hash = get_password_hash(TEST_PASSWORD)
    print(f"生成密码哈希: {password_hash[:30]}...")
    
    # 生成用户ID
    user_id = generate_user_id()
    print(f"生成用户ID: {user_id}")
    
    # 创建新的测试用户
    print("创建新的测试用户...")
    cursor.execute(
        """INSERT INTO users (user_id, username, phone, password_hash, is_active, created_at)
           VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)""",
        (user_id, TEST_USERNAME, TEST_PHONE, password_hash, 'Y')
    )
    conn.commit()
    print(f"成功创建测试用户: ID={user_id}, 用户名={TEST_USERNAME}, 手机号={TEST_PHONE}")
    
    # 验证用户是否创建成功
    cursor.execute("SELECT user_id, username, phone, is_active FROM users WHERE phone = %s", (TEST_PHONE,))
    new_user = cursor.fetchone()
    if new_user:
        print(f"验证成功 - 创建的用户信息:")
        print(f"  用户ID: {new_user[0]}")
        print(f"  用户名: {new_user[1]}")
        print(f"  手机号: {new_user[2]}")
        print(f"  状态: {new_user[3]}")
    
    # 关闭连接
    cursor.close()
    conn.close()
    print("数据库连接已关闭")
    print("清理并重新创建测试用户完成")
    
except Exception as e:
    print(f"发生错误: {e}")
    if conn:
        try:
            conn.rollback()
            conn.close()
            print("数据库连接已关闭")
        except:
            pass