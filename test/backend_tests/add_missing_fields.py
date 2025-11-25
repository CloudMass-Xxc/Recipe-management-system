import psycopg2
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接参数 - 从.env文件中的DATABASE_URL解析
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://app_user:app_password@localhost:5432/recipe_system')

# 解析DATABASE_URL获取连接参数
import urllib.parse
parsed_url = urllib.parse.urlparse(DATABASE_URL)
DB_USER = parsed_url.username
DB_PASSWORD = parsed_url.password
DB_HOST = parsed_url.hostname
DB_PORT = parsed_url.port
DB_NAME = parsed_url.path[1:]  # 去掉开头的斜杠

def connect_db():
    """连接到PostgreSQL数据库"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("成功连接到数据库")
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def add_missing_fields(conn):
    """添加缺失的字段"""
    try:
        cursor = conn.cursor()
        
        # 检查并添加phone字段
        cursor.execute("""
            DO $$ BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = 'phone'
                ) THEN
                    ALTER TABLE users ADD COLUMN phone character varying(20);
                END IF;
            END $$
        """)
        
        # 检查并添加display_name字段
        cursor.execute("""
            DO $$ BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = 'display_name'
                ) THEN
                    ALTER TABLE users ADD COLUMN display_name character varying(100);
                END IF;
            END $$
        """)
        
        conn.commit()
        print("成功添加缺失的字段")
        
    except Exception as e:
        print(f"添加字段失败: {e}")
        conn.rollback()
    finally:
        cursor.close()

def verify_fields(conn):
    """验证字段是否成功添加"""
    try:
        cursor = conn.cursor()
        
        # 查询users表的所有字段
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'users'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print("\nUsers表的字段信息:")
        for column in columns:
            print(f"字段名: {column[0]}, 数据类型: {column[1]}")
            
        # 检查phone和display_name字段是否存在
        phone_exists = any(col[0] == 'phone' for col in columns)
        display_name_exists = any(col[0] == 'display_name' for col in columns)
        
        print(f"\nphone字段存在: {phone_exists}")
        print(f"display_name字段存在: {display_name_exists}")
        
        return phone_exists and display_name_exists
        
    except Exception as e:
        print(f"验证字段失败: {e}")
        return False
    finally:
        cursor.close()

def main():
    """主函数"""
    conn = connect_db()
    if conn:
        try:
            # 添加缺失的字段
            add_missing_fields(conn)
            
            # 验证字段是否成功添加
            all_fields_added = verify_fields(conn)
            
            if all_fields_added:
                print("\n所有缺失的字段已成功添加到users表中")
            else:
                print("\n部分字段未能成功添加，请检查错误信息")
                
        finally:
            conn.close()
            print("\n数据库连接已关闭")

if __name__ == "__main__":
    main()
