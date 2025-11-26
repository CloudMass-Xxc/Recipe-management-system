import os
import psycopg2
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_db_connection():
    print("开始测试数据库连接...")
    
    # 从环境变量获取数据库连接信息
    db_url = os.getenv("DATABASE_URL")
    print(f"使用的数据库URL: {db_url}")
    
    if not db_url:
        print("错误: 未找到DATABASE_URL环境变量")
        return False
    
    try:
        # 尝试连接数据库
        conn = psycopg2.connect(db_url)
        print("成功连接到数据库!")
        
        # 获取数据库游标
        cursor = conn.cursor()
        
        # 执行简单的查询来验证连接
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"数据库版本: {db_version[0]}")
        
        # 查询所有schema中的表
        cursor.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'pg_catalog');")
        tables = cursor.fetchall()
        
        if tables:
            print("数据库中的表:")
            for schema, table in tables:
                print(f"- {schema}.{table}")
        else:
            print("警告: 数据库中没有找到表")
        
        # 关闭游标和连接
        cursor.close()
        conn.close()
        print("数据库连接已关闭")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"数据库连接失败: {e}")
        return False
    except Exception as e:
        print(f"发生错误: {e}")
        return False

if __name__ == "__main__":
    success = test_db_connection()
    print(f"\n数据库连接测试{'成功' if success else '失败'}")