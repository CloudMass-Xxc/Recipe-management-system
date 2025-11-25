#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PostgreSQL表存在性详细检查工具
用于诊断为什么app_schema.users表查询失败
"""

import psycopg2
import psycopg2.extensions

def main():
    """主函数"""
    print("=== PostgreSQL表存在性详细检查工具 ===")
    print("本工具将深入检查app_schema.users表的存在性问题")
    print("=" * 60)
    
    # 连接到系统数据库
    try:
        conn = psycopg2.connect(
            dbname='recipe_system',
            user='app_user',
            password='xxc1018',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("✅ 成功连接到recipe_system数据库")
        
        # 检查数据库中的所有schema
        print("\n📋 数据库中的所有schema:")
        cursor.execute("SELECT schema_name FROM information_schema.schemata;")
        schemas = cursor.fetchall()
        for (schema,) in schemas:
            print(f"  {schema}")
        
        # 检查app_schema是否存在
        cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = 'app_schema');")
        app_schema_exists = cursor.fetchone()[0]
        print(f"\n✅ app_schema存在: {app_schema_exists}")
        
        if app_schema_exists:
            # 检查app_schema中的所有表
            print("\n📋 app_schema中的所有表:")
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'app_schema';")
            tables = cursor.fetchall()
            
            if tables:
                print(f"找到 {len(tables)} 个表:")
                user_table_exists = False
                for (table,) in tables:
                    status = "✅" if table == "users" else "  "
                    print(f"{status} {table}")
                    if table == "users":
                        user_table_exists = True
                
                if user_table_exists:
                    print("\n✅ users表确实存在于app_schema中")
                    
                    # 检查表的所有者
                    cursor.execute("SELECT tableowner FROM pg_tables WHERE schemaname = 'app_schema' AND tablename = 'users';")
                    owner = cursor.fetchone()[0]
                    print(f"   表所有者: {owner}")
                    
                    # 检查当前用户对表的权限
                    print("\n🔍 检查表权限:")
                    permissions = ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
                    for perm in permissions:
                        cursor.execute("SELECT has_table_privilege(current_user, 'app_schema.users', %s);", (perm,))
                        has_perm = cursor.fetchone()[0]
                        print(f"   {perm} 权限: {'✅ 有' if has_perm else '❌ 没有'}")
                    
                    # 检查search_path设置
                    cursor.execute("SHOW search_path;")
                    search_path = cursor.fetchone()[0]
                    print(f"\n🔍 当前search_path设置: {search_path}")
                    
                    # 检查是否可以直接查询表
                    print("\n🔍 尝试使用完全限定名查询表:")
                    try:
                        cursor.execute("SELECT COUNT(*) FROM app_schema.users;")
                        count = cursor.fetchone()[0]
                        print(f"✅ 成功查询到 {count} 条记录")
                    except Exception as e:
                        print(f"❌ 查询失败: {e}")
                    
                    # 尝试设置search_path后查询
                    print("\n🔍 尝试设置search_path后查询:")
                    try:
                        cursor.execute("SET search_path TO app_schema, public;")
                        cursor.execute("SHOW search_path;")
                        new_search_path = cursor.fetchone()[0]
                        print(f"   新的search_path: {new_search_path}")
                        
                        cursor.execute("SELECT COUNT(*) FROM users;")
                        count = cursor.fetchone()[0]
                        print(f"✅ 成功使用非限定名查询到 {count} 条记录")
                    except Exception as e:
                        print(f"❌ 设置search_path后查询失败: {e}")
                else:
                    print("\n❌ users表不存在于app_schema中")
                    print("   可能的原因:")
                    print("   1. 表名大小写问题")
                    print("   2. 表名拼写错误")
                    print("   3. 表还未创建")
                    print("   4. 表在其他schema中")
                    
                    # 尝试查找可能的表名（忽略大小写）
                    print("\n🔍 尝试查找可能的表名（忽略大小写）:")
                    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'app_schema' AND LOWER(table_name) LIKE '%user%';")
                    possible_tables = cursor.fetchall()
                    if possible_tables:
                        print("找到可能的相关表:")
                        for (table,) in possible_tables:
                            print(f"  {table}")
                    else:
                        print("没有找到与'user'相关的表")
            else:
                print("\n❌ app_schema中没有任何表")
                print("   可能需要运行数据库迁移脚本创建表")
        
        # 检查PostgreSQL大小写敏感性设置
        print("\n🔍 PostgreSQL大小写敏感性检查:")
        print("   PostgreSQL默认区分大小写，但未加引号时会自动转小写")
        print("   例如: SELECT * FROM App_Schema.Users; 与 SELECT * FROM app_schema.users; 不同")
        
        # 检查是否存在其他可能包含users表的schema
        print("\n🔍 查找所有包含'user'表的schema:")
        cursor.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE LOWER(table_name) = 'users';")
        user_tables = cursor.fetchall()
        if user_tables:
            print("找到users表在以下位置:")
            for (schema, table) in user_tables:
                print(f"  {schema}.{table}")
        else:
            print("在任何schema中都没有找到名为'users'的表")
        
        # 检查manage_schema.py中的表创建信息
        print("\n🔍 表创建建议:")
        print("   如果表确实不存在，可以运行以下SQL创建:")
        print("   CREATE SCHEMA IF NOT EXISTS app_schema;")
        print("   CREATE TABLE app_schema.users (")
        print("       id SERIAL PRIMARY KEY,")
        print("       username VARCHAR(50) NOT NULL UNIQUE,")
        print("       email VARCHAR(100) NOT NULL UNIQUE,")
        print("       password VARCHAR(255) NOT NULL,")
        print("       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        print("   );")
        print("   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA app_schema TO app_user;")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"❌ 连接到数据库失败: {e}")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
    
    print("\n" + "=" * 60)
    print("💡 psql命令行检查表存在性:")
    print("=" * 60)
    print("1. 连接到数据库:")
    print("   psql -U app_user -d recipe_system")
    print("")
    print("2. 列出所有schema:")
    print("   \dn")
    print("")
    print("3. 列出特定schema中的表:")
    print("   \dt app_schema.*")
    print("")
    print("4. 检查表是否存在:")
    print("   SELECT EXISTS(")
    print("     SELECT FROM information_schema.tables ")
    print("     WHERE table_schema = 'app_schema' AND table_name = 'users'")
    print("   );")
    print("")
    print("5. 尝试查询表:")
    print("   SELECT * FROM app_schema.users LIMIT 10;")
    print("")
    print("6. 检查search_path:")
    print("   SHOW search_path;")
    print("   SET search_path TO app_schema, public;")
    print("   SELECT * FROM users LIMIT 10;")
    print("\n✅ 诊断完成!")

if __name__ == "__main__":
    main()