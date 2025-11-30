# 直接测试数据库查询，验证手机号查询功能

import sys
import os

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy.orm import Session
from app.core.database import engine, get_db
from app.models.user import User

# 测试手机号
test_phone = "13f4dfd834"

print(f"\n=== Testing Database Query for Phone: {test_phone} ===")

# 创建数据库会话
db = Session(engine)

try:
    # 直接调用User.get_by_phone方法
    print("1. Testing User.get_by_phone() method...")
    user_by_phone = User.get_by_phone(db, test_phone)
    print(f"Result: {user_by_phone}")
    
    # 直接使用SQLAlchemy查询
    print("\n2. Testing direct SQLAlchemy query...")
    user_direct = db.query(User).filter(User.phone == test_phone).first()
    print(f"Result: {user_direct}")
    
    # 测试其他查询方式，确认用户存在
    print("\n3. Testing email query to confirm user exists...")
    test_email = "test_f4dfd834@example.com"
    user_by_email = User.get_by_email(db, test_email)
    print(f"Result: {user_by_email}")
    if user_by_email:
        print(f"User phone from email query: {user_by_email.phone}")
    
    # 测试用户名查询
    print("\n4. Testing username query to confirm user exists...")
    test_username = "testuser_f4dfd834"
    user_by_username = User.get_by_username(db, test_username)
    print(f"Result: {user_by_username}")
    if user_by_username:
        print(f"User phone from username query: {user_by_username.phone}")
    
    # 检查所有用户的手机号
    print("\n5. Listing all users with their phone numbers...")
    all_users = db.query(User).all()
    print(f"Total users found: {len(all_users)}")
    for user in all_users[:10]:  # 只显示前10个用户
        print(f"- User: {user.username}, Phone: {user.phone}")
        
finally:
    # 关闭数据库会话
    db.close()
    print("\nDatabase session closed.")
