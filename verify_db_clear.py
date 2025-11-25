import os
from sqlalchemy import create_engine, text

# 从环境变量或.env文件获取数据库连接信息
def get_db_connection_string():
    try:
        with open('backend/.env', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('DATABASE_URL='):
                    return line.split('=', 1)[1].strip().strip('"')
    except Exception:
        pass
    
    return "postgresql://app_user:xxc1018@localhost:5432/recipe_system"

def verify_database_clear():
    print("开始验证数据库清空状态...")
    
    db_url = get_db_connection_string()
    print(f"使用数据库连接: {db_url}")
    
    try:
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            # 检查所有schema
            print("\n检查所有可用的schema:")
            result = connection.execute(text("""
                SELECT schema_name 
                FROM information_schema.schemata 
                WHERE schema_name NOT LIKE 'pg_%' AND schema_name != 'information_schema'
            """))
            schemas = [row[0] for row in result]
            print(f"找到 {len(schemas)} 个schema: {schemas}")
            
            # 检查每个schema中的表和数据量
            all_tables_empty = True
            
            for schema in schemas:
                print(f"\n检查schema '{schema}'中的表:")
                
                # 获取schema中的所有表
                tables_result = connection.execute(text(f"""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = '{schema}' 
                    ORDER BY table_name
                """))
                tables = [row[0] for row in tables_result]
                
                if not tables:
                    print(f"  schema '{schema}'中没有表")
                    continue
                
                print(f"  schema '{schema}'中有 {len(tables)} 个表:")
                
                # 检查每个表的数据量
                for table in tables:
                    try:
                        count_result = connection.execute(text(f"SELECT COUNT(*) FROM {schema}.{table}"))
                        count = count_result.scalar()
                        print(f"  - {schema}.{table}: {count} 条记录")
                        
                        if count > 0:
                            all_tables_empty = False
                            print(f"    ⚠️  表 {schema}.{table} 不为空！")
                            
                    except Exception as e:
                        print(f"  - 检查表 {schema}.{table} 时出错: {e}")
            
            # 最终结论
            print("\n=== 验证结果 ===")
            if all_tables_empty:
                print("✅ 数据库已完全清空！所有表都没有数据。")
            else:
                print("❌ 数据库中仍有不为空的表。")
                
    except Exception as e:
        print(f"❌ 验证过程中发生错误: {e}")

if __name__ == "__main__":
    verify_database_clear()