from app.models.user import User
from app.core.database import SessionLocal

# 创建数据库连接
db = SessionLocal()

# 查询所有用户
try:
    users = db.query(User).all()
    print(f'用户总数: {len(users)}')
    
    for user in users:
        print(f'用户ID: {user.user_id}, 用户名: {user.username}, 邮箱: {user.email}, 手机号: {user.phone}, 状态: {user.is_active}')
finally:
    # 关闭数据库连接
    db.close()