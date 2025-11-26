import psycopg2
from passlib.context import CryptContext

# 创建正确的密码上下文（与后端相同）
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

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
    
    # 测试密码
    test_password = "password123"
    
    # 生成正确的密码哈希（使用与后端相同的算法）
    hashed_password = pwd_context.hash(test_password[:72])
    print(f"生成的密码哈希: {hashed_password}")
    
    # 更新测试用户的密码哈希
    target_phone = "13160697108"
    print(f"\n正在更新手机号为 {target_phone} 的用户密码...")
    
    cur.execute(
        "UPDATE users SET password_hash = %s WHERE phone = %s;",
        (hashed_password, target_phone)
    )
    
    if cur.rowcount > 0:
        print(f"✓ 成功更新用户密码！")
        print(f"  手机号: {target_phone}")
        print(f"  密码: {test_password}")
        print(f"  密码哈希已更新为 pbkdf2_sha256 格式")
    else:
        print(f"! 未找到手机号为 {target_phone} 的用户")
    
    # 关闭连接
    cur.close()
    conn.close()
    
    print("\n操作完成！")
    
except Exception as e:
    print(f"数据库操作错误: {e}")
