import psycopg2
import os

def analyze_database_structure():
    print("开始分析数据库结构...")
    
    # 数据库连接信息
    db_params = {
        'host': 'localhost',
        'database': 'recipe_system',
        'user': 'app_user',
        'password': 'xxc1018',
        'port': '5432'
    }
    
    connection = None
    cursor = None
    
    try:
        # 连接到数据库
        print("正在连接数据库...")
        connection = psycopg2.connect(**db_params)
        connection.autocommit = True
        cursor = connection.cursor()
        
        print("数据库连接成功！")
        
        # 查询所有表
        print("\n1. 查询数据库中的所有表：")
        cursor.execute("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog') 
            ORDER BY table_schema, table_name;
        """)
        
        tables = cursor.fetchall()
        if tables:
            print(f"找到 {len(tables)} 个表：")
            for schema, table in tables:
                print(f"- {schema}.{table}")
                
                # 查询每个表的结构
                print(f"  表 {table} 的结构：")
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_schema = %s AND table_name = %s
                    ORDER BY ordinal_position;
                """, (schema, table))
                
                columns = cursor.fetchall()
                for col_name, data_type, is_nullable in columns:
                    print(f"    - {col_name} ({data_type}, 可空: {is_nullable})")
                
                # 查询外键关系
                cursor.execute("""
                    SELECT 
                        tc.table_name AS source_table,
                        kcu.column_name AS source_column,
                        ccu.table_name AS target_table,
                        ccu.column_name AS target_column
                    FROM 
                        information_schema.table_constraints AS tc
                        JOIN information_schema.key_column_usage AS kcu
                          ON tc.constraint_name = kcu.constraint_name
                          AND tc.table_schema = kcu.table_schema
                        JOIN information_schema.constraint_column_usage AS ccu
                          ON ccu.constraint_name = tc.constraint_name
                          AND ccu.table_schema = tc.table_schema
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                      AND tc.table_schema = %s
                      AND tc.table_name = %s;
                """, (schema, table))
                
                foreign_keys = cursor.fetchall()
                if foreign_keys:
                    print("    外键关系：")
                    for source_table, source_col, target_table, target_col in foreign_keys:
                        print(f"      - {source_col} 引用 {target_table}.{target_col}")
                else:
                    print("    无外键关系")
                
                # 查询表的记录数
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {schema}.{table};")
                    count = cursor.fetchone()[0]
                    print(f"    记录数: {count}")
                except Exception as e:
                    print(f"    无法获取记录数: {e}")
                
                print()
        else:
            print("数据库中没有找到表")
    
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭连接
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("数据库连接已关闭")

if __name__ == "__main__":
    analyze_database_structure()
