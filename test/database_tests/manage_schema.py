#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PostgreSQL Schema管理工具
用于检查、切换和管理PostgreSQL中的schema
"""

import psycopg2
import sys

def connect_to_database():
    """连接到PostgreSQL数据库"""
    print("=== PostgreSQL Schema管理工具 ===")
    print("连接到recipe_system数据库...")
    
    # 使用之前成功连接的数据库信息
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
        print("✅ 数据库连接成功!")
        return conn, cursor
    except psycopg2.OperationalError as e:
        print(f"❌ 数据库连接失败: {e}")
        print("请检查数据库连接信息是否正确")
        sys.exit(1)

def list_all_schemas(cursor):
    """列出数据库中的所有schema"""
    print("\n📋 列出所有schema:")
    print("-" * 50)
    
    cursor.execute("SELECT schema_name FROM information_schema.schemata ORDER BY schema_name")
    schemas = cursor.fetchall()
    
    for i, (schema_name,) in enumerate(schemas, 1):
        print(f"{i:2d}. {schema_name}")
    
    print("-" * 50)
    print(f"总计找到 {len(schemas)} 个schema")
    return schemas

def check_schema_exists(cursor, schema_name):
    """检查指定的schema是否存在"""
    print(f"\n🔍 检查schema '{schema_name}' 是否存在...")
    
    cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = %s)",
        (schema_name,)
    )
    exists = cursor.fetchone()[0]
    
    if exists:
        print(f"✅ Schema '{schema_name}' 存在")
    else:
        print(f"❌ Schema '{schema_name}' 不存在")
    return exists

def show_current_search_path(cursor):
    """显示当前的search_path"""
    cursor.execute("SHOW search_path")
    search_path = cursor.fetchone()[0]
    print(f"\n📌 当前search_path: {search_path}")
    return search_path

def set_search_path(cursor, schema_name):
    """设置search_path以进入特定schema"""
    print(f"\n🔄 设置search_path到 '{schema_name}, public'...")
    
    try:
        cursor.execute(f"SET search_path TO {schema_name}, public")
        print(f"✅ search_path已设置为: {schema_name}, public")
        print("现在可以直接查询该schema下的表，无需指定schema前缀")
        return True
    except Exception as e:
        print(f"❌ 设置search_path失败: {e}")
        return False

def list_tables_in_schema(cursor, schema_name):
    """列出指定schema中的所有表"""
    print(f"\n📋 列出 '{schema_name}' schema中的所有表:")
    print("-" * 50)
    
    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = %s ORDER BY table_name",
        (schema_name,)
    )
    tables = cursor.fetchall()
    
    if tables:
        for i, (table_name,) in enumerate(tables, 1):
            print(f"{i:2d}. {table_name}")
        print("-" * 50)
        print(f"总计找到 {len(tables)} 个表")
    else:
        print(f"❌ 在 '{schema_name}' schema中没有找到任何表")
    
    return tables

def main():
    """主函数"""
    conn, cursor = connect_to_database()
    
    try:
        # 列出所有schema
        list_all_schemas(cursor)
        
        # 显示当前search_path
        show_current_search_path(cursor)
        
        # 检查app_schema是否存在
        schema_to_check = 'app_schema'
        exists = check_schema_exists(cursor, schema_to_check)
        
        if exists:
            # 如果存在，设置search_path
            set_search_path(cursor, schema_to_check)
            # 列出该schema中的表
            list_tables_in_schema(cursor, schema_to_check)
            
            # 提供如何使用完全限定名访问表的示例
            print("\n💡 提示: 您也可以使用完全限定名直接访问表:")
            print(f"  例如: SELECT * FROM {schema_to_check}.users;")
        else:
            # 如果不存在，提供创建schema的选项
            print("\n💡 如果需要创建app_schema，请使用以下SQL命令:")
            print("  CREATE SCHEMA app_schema;")
            print("\n或者，您可以直接在public schema中操作，这是PostgreSQL的默认schema")
            
            # 列出public schema中的表
            print("\n📋 列出 'public' schema中的所有表:")
            list_tables_in_schema(cursor, 'public')
        
        # 总结如何管理schema
        print("\n📝 进入特定schema的方法总结:")
        print("1. 临时设置search_path: SET search_path TO schema_name, public;")
        print("2. 使用完全限定名: schema_name.table_name")
        print("3. 永久设置用户的search_path: ALTER USER username SET search_path TO schema_name, public;")
        
    finally:
        cursor.close()
        conn.close()
        print("\n✅ 数据库连接已关闭")

if __name__ == "__main__":
    main()