import psycopg2

# 连接到数据库
conn = psycopg2.connect(
    dbname='recipe_system',
    user='app_user',
    password='xxc1018',
    host='localhost',
    port='5432'
)
conn.autocommit = True
cursor = conn.cursor()

print('=== 用户表结构 ===')
cursor.execute('SELECT column_name, data_type FROM information_schema.columns WHERE table_name = \'users\' ORDER BY ordinal_position')
columns = cursor.fetchall()
for col in columns:
    print(f'{col[0]}: {col[1]}')

print('\n=== 用户数据 ===')
cursor.execute('SELECT user_id, username, email, is_active FROM users')
users = cursor.fetchall()
print(f'找到 {len(users)} 个用户')
for user in users:
    print(f'用户ID: {user[0]}, 用户名: {user[1]}, 邮箱: {user[2]}, 激活状态: {user[3]}')

# 检查是否有表结构更新脚本
print('\n=== 检查更新脚本 ===')
import os
if os.path.exists('add_phone_column.py'):
    print('发现 add_phone_column.py 脚本')
else:
    print('未发现 add_phone_column.py 脚本')

# 检查schema设置
print('\n=== 检查schema设置 ===')
cursor.execute('SHOW search_path')
search_path = cursor.fetchone()[0]
print(f'当前search_path: {search_path}')

cursor.close()
conn.close()