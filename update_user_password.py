from sqlalchemy.orm import Session
from app.core.database import engine, Base
from app.models.user import User
from app.auth.password import get_password_hash

# 要更新的用户手机号和新密码
TARGET_PHONE = "15800152125"
NEW_PASSWORD = "password123"

def update_user_password():
    # 创建数据库会话
    session = Session(engine)
    
    try:
        # 查找用户
        user = session.query(User).filter(User.phone == TARGET_PHONE).first()
        
        if user:
            print(f"找到用户: {user.display_name}, 手机号: {user.phone}")
            print(f"当前密码哈希值: {user.password_hash}")
            
            # 生成新密码的哈希值
            new_password_hash = get_password_hash(NEW_PASSWORD)
            print(f"新密码哈希值: {new_password_hash}")
            
            # 更新密码
            user.password_hash = new_password_hash
            session.commit()
            print(f"✅ 成功更新用户 {TARGET_PHONE} 的密码为 '{NEW_PASSWORD}'")
        else:
            print(f"❌ 未找到手机号为 {TARGET_PHONE} 的用户")
    
    except Exception as e:
        print(f"❌ 更新密码时出错: {str(e)}")
        session.rollback()
    
    finally:
        session.close()

if __name__ == "__main__":
    print(f"开始更新用户密码")
    update_user_password()
    print("操作完成")
