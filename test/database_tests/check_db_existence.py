#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PostgreSQL数据库存在性检查工具
用于诊断为什么在PostgreSQL中查询不到系统使用的数据库
"""

import psycopg2
import psycopg2.extensions
import sys

def main():
    """主函数"""
    print("=== PostgreSQL数据库存在性检查工具 ===")
    print("本工具将帮助诊断为什么在PostgreSQL中查询不到系统使用的数据库")
    print("=" * 60)
    
    # 系统使用的数据库名称
    system_db_name = 'recipe_system'
    print(f"\n📌 系统配置使用的数据库名: {system_db_name}")
    
    # 尝试连接到PostgreSQL服务器（不指定数据库）
    print("\n🔍 尝试连接到PostgreSQL服务器（不指定具体数据库）...")
    try:
        # 先连接到默认的postgres数据库
        conn = psycopg2.connect(
            dbname='postgres',  # 使用默认的postgres管理数据库
            user='app_user',
            password='xxc1018',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("✅ 成功连接到PostgreSQL服务器")
        
        # 列出所有可用的数据库
        print("\n📋 列出所有可用的数据库:")
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()
        print(f"找到 {len(databases)} 个数据库:")
        
        system_db_exists = False
        for (db,) in databases:
            status = "✅" if db == system_db_name else "  "
            print(f"{status} {db}")
            if db == system_db_name:
                system_db_exists = True
        
        if system_db_exists:
            print(f"\n✅ 确认: {system_db_name} 数据库确实存在")
            
            # 获取数据库的所有者信息
            cursor.execute("SELECT pg_catalog.pg_get_userbyid(datdba) FROM pg_database WHERE datname = %s;", (system_db_name,))
            owner = cursor.fetchone()[0]
            print(f"   数据库所有者: {owner}")
            
            # 检查当前用户对数据库的权限
            cursor.execute("SELECT has_database_privilege(current_user, %s, 'CONNECT');", (system_db_name,))
            has_connect = cursor.fetchone()[0]
            print(f"   当前用户(app_user)是否有权限连接: {'✅ 有' if has_connect else '❌ 没有'}")
            
        else:
            print(f"\n❌ 错误: {system_db_name} 数据库不存在")
            print("   可能的解决方案:")
            print("   1. 检查数据库是否已创建")
            print("   2. 检查连接参数是否正确")
            print("   3. 检查PostgreSQL服务是否运行在正确的端口上")
            
            # 提供创建数据库的SQL
            print("\n💡 创建数据库的命令:")
            print(f"   CREATE DATABASE {system_db_name};")
            print(f"   CREATE USER app_user WITH PASSWORD 'xxc1018';")
            print(f"   GRANT ALL PRIVILEGES ON DATABASE {system_db_name} TO app_user;")
        
        # 检查PostgreSQL版本
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"\nℹ️ PostgreSQL版本信息: {version.split(',')[0]}")
        
        # 检查PostgreSQL服务状态
        print(f"\nℹ️ 当前连接信息:")
        print(f"   主机: localhost")
        print(f"   端口: 5432")
        print(f"   当前用户名: app_user")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"❌ 连接到PostgreSQL服务器失败: {e}")
        print("\n🔍 尝试使用postgres超级用户连接...")
        
        try:
            # 尝试使用postgres用户连接
            conn = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='password',  # 假设默认密码
                host='localhost',
                port='5432'
            )
            conn.autocommit = True
            cursor = conn.cursor()
            print("✅ 成功使用postgres用户连接")
            
            # 列出所有数据库
            print("\n📋 列出所有可用的数据库:")
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            databases = cursor.fetchall()
            print(f"找到 {len(databases)} 个数据库:")
            for (db,) in databases:
                print(f"  {db}")
            
            cursor.close()
            conn.close()
            
        except Exception as e2:
            print(f"❌ postgres用户连接也失败: {e2}")
            print("\n⚠️ 可能的问题:")
            print("   1. PostgreSQL服务未运行")
            print("   2. 连接参数错误（主机、端口、用户名、密码）")
            print("   3. PostgreSQL未正确安装")
            print("   4. 防火墙阻止了连接")
    
    # 测试直接连接到系统数据库
    print("\n" + "=" * 60)
    print(f"🔍 尝试直接连接到 {system_db_name} 数据库...")
    try:
        conn = psycopg2.connect(
            dbname=system_db_name,
            user='app_user',
            password='xxc1018',
            host='localhost',
            port='5432'
        )
        print(f"✅ 成功连接到 {system_db_name} 数据库")
        
        # 获取数据库中的schema
        cursor = conn.cursor()
        cursor.execute("SELECT schema_name FROM information_schema.schemata;")
        schemas = cursor.fetchall()
        print(f"\n📋 数据库中的schema:")
        for (schema,) in schemas:
            print(f"  {schema}")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"❌ 无法连接到 {system_db_name} 数据库: {e}")
        print("\n💡 可能的解决方案:")
        print("   1. 确保数据库已创建: CREATE DATABASE recipe_system;")
        print("   2. 确保用户有权限: GRANT ALL PRIVILEGES ON DATABASE recipe_system TO app_user;")
        print("   3. 检查用户名和密码是否正确")
        print("   4. 检查PostgreSQL服务是否正在运行")
    
    # 提供psql命令行操作建议
    print("\n" + "=" * 60)
    print("💡 psql命令行操作指南:")
    print("=" * 60)
    print("1. 列出所有数据库:")
    print("   psql -U postgres -c '\l'")
    print("   或登录后执行: \l")
    print("")
    print("2. 连接到特定数据库:")
    print(f"   psql -U app_user -d {system_db_name}")
    print("   或登录后执行: \c recipe_system")
    print("")
    print("3. 查看当前连接信息:")
    print("   SELECT current_database(), current_user;")
    print("")
    print("4. 如果数据库不存在，创建数据库（需要管理员权限）:")
    print("   psql -U postgres")
    print(f"   CREATE DATABASE {system_db_name};")
    print(f"   CREATE USER app_user WITH PASSWORD 'xxc1018';")
    print(f"   GRANT ALL PRIVILEGES ON DATABASE {system_db_name} TO app_user;")
    print("   \q")
    
    print("\n✅ 诊断完成!")

if __name__ == "__main__":
    main()