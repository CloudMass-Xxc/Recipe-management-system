import os
import psycopg2
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def check_db_structure():
    print("开始检查数据库结构...")
    
    db_url = os.getenv("DATABASE_URL")
    
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # 检查所有schema
        print("\n数据库中的Schema:")
        cursor.execute("SELECT schema_name FROM information_schema.schemata;")
        schemas = cursor.fetchall()
        for schema in schemas:
            print(f"- {schema[0]}")
        
        # 检查public schema中的表
        print("\nPublic schema中的表:")
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cursor.fetchall()
        if tables:
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("- 没有找到表")
        
        # 检查是否有app_schema（从SQL文件中看到使用了这个schema）
        print("\n检查app_schema中的表:")
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'app_schema';")
        app_schema_tables = cursor.fetchall()
        if app_schema_tables:
            for table in app_schema_tables:
                print(f"- {table[0]}")
        else:
            print("- app_schema中没有找到表")
        
        # 检查是否需要创建表结构
        print("\n分析结果:")
        if not tables and not app_schema_tables:
            print("数据库中没有表结构，需要创建。")
            print("建议按照PostgreSQL数据库配置指南中的步骤创建表结构。")
        else:
            print("数据库中已存在表结构。")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    check_db_structure()