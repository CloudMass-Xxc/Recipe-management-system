from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.user import User
from app.auth.password import get_password_hash

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # 查找用户
    email = 'xxiaochang@qq.com'
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        print(f"找到用户: {user.username} (ID: {user.user_id})")
        print(f"当前密码哈希: {user.password_hash}")
        
        # 重置密码为'testpassword'
        new_password = 'testpassword'
        new_hash = get_password_hash(new_password)
        print(f"新密码哈希: {new_hash}")
        
        # 更新用户密码
        user.password_hash = new_hash
        db.commit()
        print(f"用户 {user.username} 的密码已重置为 '{new_password}'")
    else:
        print(f"未找到邮箱为 {email} 的用户")
        
    # 测试所有用户
    print("\n所有用户信息:")
    users = db.query(User).all()
    for u in users:
        print(f"- {u.username} ({u.email}): {u.password_hash}")
        
except Exception as e:
    print(f"发生错误: {e}")
    db.rollback()
finally:
    db.close()
