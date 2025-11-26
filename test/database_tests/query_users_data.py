#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
查询users表所有数据的Python脚本
"""

import psycopg2
from psycopg2 import OperationalError

# 数据库连接参数（从搜索结果中提取）
DB_CONFIGS = [
    {
        'host': 'localhost',
        'database': 'recipe_system',
        'user': 'app_user',
        'password': 'xxc1018',
        'port': '5432'
    },
    {
        'host': 'localhost',
        'database': 'recipe_system',
        'user': 'postgres',
        'password': 'xxc1018',
        'port': '5432'
    }
]

# 可能的表名和schema组合
POSSIBLE_TABLE_NAMES = [
    'app_schema.users',
    'users',
    'public.users'
]

def connect_to_db(config):
    """连接到数据库"""
    try:
        print(f"尝试连接到数据库 (用户: {config['user']})...")
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        print("✅ 数据库连接成功!")
        return conn
    except OperationalError as e:
        print(f"❌ 数据库连接失败: {e}")
        return None

def query_users_data(conn):
    """查询users表的所有数据"""
    try:
        cursor = conn.cursor()
        
        # 检查schema和表结构
        print("\n🔍 检查数据库结构:")
        
        # 1. 检查所有schema
        print("\n📋 数据库中的所有schema:")
        cursor.execute("SELECT schema_name FROM information_schema.schemata;")
        schemas = cursor.fetchall()
        for (schema,) in schemas:
            print(f"  {schema}")
        
        # 2. 检查users表的存在性
        found = False
        for table_name in POSSIBLE_TABLE_NAMES:
            print(f"\n检查表: {table_name}")
            
            # 提取schema和表名
            if '.' in table_name:
                schema, name = table_name.split('.')
                query = f"""
                SELECT EXISTS(
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_schema = '{schema}' 
                    AND table_name = '{name}'
                )
                """
            else:
                query = f"""
                SELECT EXISTS(
                    SELECT 1 
                    FROM information_schema.tables 
                    WHERE table_name = '{table_name}'
                )
                """
            
            try:
                cursor.execute(query)
                exists = cursor.fetchone()[0]
                
                if exists:
                    print(f"✅ 表 {table_name} 存在!")
                    found = True
                    
                    # 3. 获取表结构
                    print("\n📋 表结构:")
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0;")
                    columns = [desc[0] for desc in cursor.description]
                    print(f"  字段: {', '.join(columns)}")
                    
                    # 4. 查询所有数据
                    print(f"\n📊 查询 {table_name} 表的所有数据:")
                    cursor.execute(f"SELECT * FROM {table_name};")
                    rows = cursor.fetchall()
                    
                    print(f"\n找到 {len(rows)} 条用户记录:")
                    print("-" * 120)
                    
                    # 打印表头
                    header = " | ".join([f"{col:<15}" for col in columns])
                    print(f"{header}")
                    print("-" * 120)
                    
                    # 打印数据行
                    for row in rows:
                        # 将元组转换为字符串列表，处理None值
                        row_str = []
                        for i, value in enumerate(row):
                            col_name = columns[i]
                            # 对敏感字段进行部分隐藏
                            if col_name in ['password_hash']:
                                if value:
                                    row_str.append(f"{'[哈希值]':<15}")
                                else:
                                    row_str.append(f"{'':<15}")
                            else:
                                # 其他字段正常显示，但限制长度
                                str_value = str(value) if value is not None else ""
                                if len(str_value) > 15:
                                    str_value = str_value[:12] + "..."
                                row_str.append(f"{str_value:<15}")
                        
                        print(f"{' | '.join(row_str)}")
                    
                    print("-" * 120)
                    print(f"\n✅ 查询完成! 共找到 {len(rows)} 条记录。")
                    break
                else:
                    print(f"❌ 表 {table_name} 不存在")
            except Exception as e:
                print(f"❌ 查询表 {table_name} 时出错: {e}")
        
        if not found:
            print("\n❌ 未找到任何users表!")
            
            # 尝试查找所有包含"user"的表
            print("\n🔍 搜索所有包含'user'的表:")
            cursor.execute("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_name ILIKE '%user%'
            """)
            user_tables = cursor.fetchall()
            
            if user_tables:
                print("找到相关表:")
                for schema, table in user_tables:
                    print(f"  {schema}.{table}")
            else:
                print("  没有找到包含'user'的表")
            
            # 列出所有表
            print("\n📋 数据库中的所有表:")
            cursor.execute("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            """)
            all_tables = cursor.fetchall()
            
            if all_tables:
                print("找到以下表:")
                for schema, table in all_tables:
                    print(f"  {schema}.{table}")
            else:
                print("  没有找到任何用户表")
        
        cursor.close()
    except Exception as e:
        print(f"❌ 执行查询时出错: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 查询users表所有数据")
    print("=" * 60)
    
    # 尝试使用不同的数据库配置
    for i, config in enumerate(DB_CONFIGS):
        print(f"\n📦 尝试配置 {i+1}/{len(DB_CONFIGS)}:")
        print(f"   用户: {config['user']}")
        print(f"   数据库: {config['database']}")
        
        conn = connect_to_db(config)
        if conn:
            try:
                query_users_data(conn)
                break
            finally:
                conn.close()
                print("\n📤 数据库连接已关闭")
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("✅ 查询完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()