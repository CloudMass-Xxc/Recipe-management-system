import os
import sqlalchemy
from app.core.config import settings
from app.core.database import engine

def test_db_interaction():
    print("开始测试数据库交互功能...")
    
    try:
        # 创建连接
        with engine.connect() as conn:
            print(f"成功连接到数据库")
            print(f"使用的schema: {settings.DATABASE_SCHEMA}")
            
            # 查询app_schema中的表
            print("\n查询app_schema中的表:")
            query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = :schema
            ORDER BY table_name
            """
            result = conn.execute(sqlalchemy.text(query), {"schema": settings.DATABASE_SCHEMA})
            tables = result.fetchall()
            
            if tables:
                print(f"找到 {len(tables)} 个表:")
                for table in tables:
                    print(f"- {table[0]}")
                    
                    # 检查每个表的记录数
                    count_query = sqlalchemy.text(f"SELECT COUNT(*) FROM {settings.DATABASE_SCHEMA}.{table[0]}")
                    count_result = conn.execute(count_query)
                    count = count_result.scalar()
                    print(f"  记录数: {count}")
            else:
                print("没有找到表")
            
            # 测试简单的查询操作
            print("\n测试简单查询操作:")
            if 'recipes' in [t[0] for t in tables]:
                test_query = sqlalchemy.text(f"SELECT * FROM {settings.DATABASE_SCHEMA}.recipes LIMIT 5")
                try:
                    test_result = conn.execute(test_query)
                    print(f"成功查询recipes表")
                    # 获取列名
                    columns = test_result.keys()
                    print(f"表结构: {', '.join(columns)}")
                except Exception as e:
                    print(f"查询recipes表时出错: {e}")
            
            print("\n数据库交互测试成功!")
            return True
            
    except Exception as e:
        print(f"数据库交互测试失败: {e}")
        return False

if __name__ == "__main__":
    test_db_interaction()