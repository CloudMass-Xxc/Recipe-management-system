"""
使用SQLAlchemy添加缺失的phone和display_name字段到users表
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# 加载环境变量
load_dotenv()

# 使用postgres用户连接数据库
database_url = 'postgresql://postgres:postgres@localhost:5432/recipe_system'
print(f"使用的数据库URL: {database_url}")

def add_missing_fields():
    """添加缺失的字段到users表"""
    try:
        # 创建数据库引擎
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # 使用inspect检查表结构
            inspector = inspect(engine)
            user_columns = [column['name'] for column in inspector.get_columns('users')]
            
            print(f"当前users表的字段: {', '.join(user_columns)}")
            
            # 添加phone字段（如果不存在）
            if 'phone' not in user_columns:
                try:
                    conn.execute(text("ALTER TABLE users ADD COLUMN phone character varying(20);"))
                    conn.commit()
                    print("成功添加phone字段")
                except SQLAlchemyError as e:
                    conn.rollback()
                    print(f"添加phone字段失败: {e}")
            else:
                print("phone字段已存在")
            
            # 添加display_name字段（如果不存在）
            if 'display_name' not in user_columns:
                try:
                    conn.execute(text("ALTER TABLE users ADD COLUMN display_name character varying(100);"))
                    conn.commit()
                    print("成功添加display_name字段")
                except SQLAlchemyError as e:
                    conn.rollback()
                    print(f"添加display_name字段失败: {e}")
            else:
                print("display_name字段已存在")
            
            # 验证字段是否添加成功
            print("\n更新后的users表字段:")
            updated_columns = [column['name'] for column in inspector.get_columns('users')]
            print(', '.join(updated_columns))
            
            # 检查是否成功添加了所需的字段
            phone_exists = 'phone' in updated_columns
            display_name_exists = 'display_name' in updated_columns
            
            print(f"\nphone字段存在: {phone_exists}")
            print(f"display_name字段存在: {display_name_exists}")
            
            if phone_exists and display_name_exists:
                print("\n✅ 所有缺失的字段已成功添加到users表")
            else:
                print("\n❌ 部分字段未能成功添加")
                
    except Exception as e:
        print(f"数据库操作失败: {e}")

if __name__ == "__main__":
    print("开始添加缺失的字段到users表...")
    add_missing_fields()
