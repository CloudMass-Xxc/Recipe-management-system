#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PostgreSQL数据库访问诊断工具
用于诊断为什么无法访问app_schema.users表
"""

import psycopg2
import sys
import os

def connect_to_database():
    """使用不同用户连接到PostgreSQL数据库"""
    print("=== PostgreSQL数据库访问诊断工具 ===")
    print("本工具将帮助诊断为什么无法访问app_schema.users表")
    print("=" * 60)
    
    # 测试多个可能的连接配置
    connection_configs = [
        {
            'name': '默认用户配置 (app_user)',
            'dbname': 'recipe_system',
            'user': 'app_user',
            'password': 'xxc1018',
            'host': 'localhost',
            'port': '5432'
        },
        {
            'name': '管理员配置 (postgres)',
            'dbname': 'recipe_system',
            'user': 'postgres',
            'password': 'password',  # 请根据实际情况修改
            'host': 'localhost',
            'port': '5432'
        }
    ]
    
    connections = []
    for config in connection_configs:
        try:
            # 分离name字段，psycopg2不接受这个参数
            config_name = config['name']
            conn_params = {k: v for k, v in config.items() if k != 'name'}
            
            print(f"\n🔍 尝试使用 {config_name} 连接...")
            conn = psycopg2.connect(**conn_params)
            conn.autocommit = True
            cursor = conn.cursor()
            print(f"✅ 连接成功! 用户: {conn_params['user']}, 数据库: {conn_params['dbname']}")
            connections.append((cursor, conn, conn_params['user']))
        except psycopg2.OperationalError as e:
            print(f"❌ 连接失败: {e}")
    
    if not connections:
        print("\n❌ 无法建立任何数据库连接")
        sys.exit(1)
    
    return connections

def check_schema_permissions(cursor, username):
    """检查用户对schema的权限"""
    print(f"\n🔍 检查用户 '{username}' 对app_schema的权限:")
    
    try:
        # 检查用户对app_schema的权限
        cursor.execute("""
            SELECT privilege_type 
            FROM information_schema.role_table_grants 
            WHERE grantee = %s 
            AND table_schema = 'app_schema'
            LIMIT 5
        """, (username,))
        permissions = cursor.fetchall()
        
        if permissions:
            print(f"✅ 用户 '{username}' 对app_schema有以下权限:")
            for (perm,) in permissions:
                print(f"   - {perm}")
        else:
            print(f"⚠️ 用户 '{username}' 对app_schema可能没有直接权限")
            
        # 检查是否有使用schema的权限
        cursor.execute("""
            SELECT has_schema_privilege(%s, 'app_schema', 'USAGE')
        """, (username,))
        has_usage = cursor.fetchone()[0]
        
        if has_usage:
            print(f"✅ 用户 '{username}' 有app_schema的USAGE权限")
        else:
            print(f"❌ 用户 '{username}' 没有app_schema的USAGE权限")
            print("   解决方案: 执行 GRANT USAGE ON SCHEMA app_schema TO username;")
            
    except Exception as e:
        print(f"查询权限时出错: {e}")

def check_table_existence(cursor):
    """检查users表的实际存在情况"""
    print("\n🔍 检查表 'app_schema.users' 的实际存在情况:")
    
    # 使用information_schema检查表是否存在
    cursor.execute("""
        SELECT EXISTS(
            SELECT 1 
            FROM information_schema.tables 
            WHERE table_schema = 'app_schema' 
            AND table_name = 'users'
        )
    """)
    exists = cursor.fetchone()[0]
    
    if exists:
        print("✅ 'app_schema.users' 表确实存在")
        
        # 获取表的所有者信息
        cursor.execute("""
            SELECT tableowner 
            FROM pg_tables 
            WHERE schemaname = 'app_schema' 
            AND tablename = 'users'
        """)
        owner = cursor.fetchone()
        if owner:
            print(f"   表所有者: {owner[0]}")
        
        # 尝试直接查询表（测试访问权限）
        try:
            cursor.execute("SELECT COUNT(*) FROM app_schema.users")
            count = cursor.fetchone()[0]
            print(f"✅ 成功查询到 {count} 条记录")
        except Exception as e:
            print(f"❌ 无法查询表内容: {e}")
            print("   可能是权限问题，请确保用户有SELECT权限")
    else:
        print("❌ 'app_schema.users' 表不存在")
        # 搜索所有schema中的users表
        print("\n🔍 在所有schema中搜索users表:")
        cursor.execute("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_name = 'users'
        """)
        tables = cursor.fetchall()
        if tables:
            print("找到以下users表:")
            for schema, table in tables:
                print(f"   - {schema}.{table}")
        else:
            print("数据库中没有名为'users'的表")

def check_current_search_path(cursor):
    """检查当前的search_path"""
    print("\n🔍 检查当前的search_path:")
    cursor.execute("SHOW search_path")
    search_path = cursor.fetchone()[0]
    print(f"当前search_path: {search_path}")
    
    if 'app_schema' in search_path:
        print("✅ app_schema已在search_path中")
    else:
        print("❌ app_schema不在search_path中")
        print("   解决方案1: SET search_path TO app_schema, public;")
        print("   解决方案2: 使用完全限定名 app_schema.users")

def check_case_sensitivity(cursor):
    """检查大小写敏感性问题"""
    print("\n🔍 检查大小写敏感性问题:")
    
    # 列出所有表名，检查是否存在大小写变体
    cursor.execute("""
        SELECT table_schema, table_name 
        FROM information_schema.tables 
        WHERE LOWER(table_name) = 'users'
    """)
    all_users_tables = cursor.fetchall()
    
    if len(all_users_tables) > 1:
        print("⚠️ 发现多个大小写不同的'users'表:")
        for schema, table in all_users_tables:
            print(f"   - {schema}.{table}")
    elif all_users_tables:
        schema, table = all_users_tables[0]
        if table != 'users':
            print(f"⚠️ 表名是 '{table}' 而不是 'users' (大小写不同)")
            print(f"   解决方案: 使用正确的大小写 {schema}.{table}")

def provide_solutions():
    """提供常见问题的解决方案"""
    print("\n" + "=" * 60)
    print("💡 常见解决方案汇总:")
    print("=" * 60)
    
    solutions = [
        {
            '问题': '权限问题',
            '解决步骤': [
                '1. 以管理员身份登录: psql -U postgres',
                '2. 连接到数据库: \c recipe_system',
                '3. 授予权限: GRANT USAGE ON SCHEMA app_schema TO app_user;',
                '4. 授予表权限: GRANT SELECT ON app_schema.users TO app_user;'  
            ]
        },
        {
            '问题': 'search_path问题',
            '解决步骤': [
                '1. 临时设置: SET search_path TO app_schema, public;',
                '2. 永久设置: ALTER USER app_user SET search_path TO app_schema, public;'  
            ]
        },
        {
            '问题': '表名大小写问题',
            '解决步骤': [
                '1. PostgreSQL表名默认小写',
                '2. 如果表名有特殊大小写，使用引号: SELECT * FROM "Users";'  
            ]
        },
        {
            '问题': '数据库连接问题',
            '解决步骤': [
                '1. 确认连接的是正确数据库: \c recipe_system',
                '2. 检查用户名和密码',
                '3. 检查主机和端口设置'  
            ]
        }
    ]
    
    for solution in solutions:
        print(f"\n🔧 {solution['问题']}:")
        for step in solution['解决步骤']:
            print(f"   {step}")

def create_test_script():
    """创建一个SQL测试脚本"""
    sql_content = """
-- PostgreSQL表访问测试脚本
-- 保存为test_table_access.sql并使用: psql -U 用户名 -d recipe_system -f test_table_access.sql

-- 1. 检查当前连接信息
SELECT current_user AS "当前用户", current_database() AS "当前数据库";

-- 2. 检查search_path
SHOW search_path;

-- 3. 尝试设置search_path
SET search_path TO app_schema, public;
SHOW search_path;

-- 4. 检查表是否存在
SELECT EXISTS(
    SELECT 1 
    FROM information_schema.tables 
    WHERE table_schema = 'app_schema' 
    AND table_name = 'users'
) AS "表是否存在";

-- 5. 在所有schema中搜索users表
SELECT table_schema, table_name 
FROM information_schema.tables 
WHERE LOWER(table_name) = 'users';

-- 6. 尝试查询表（如果存在）
DO $$
BEGIN
    IF EXISTS(
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_schema = 'app_schema' 
        AND table_name = 'users'
    ) THEN
        RAISE NOTICE '尝试查询app_schema.users表...';
        -- 注意：下面的查询会在执行时失败，如果没有权限
        -- 取消注释以测试实际查询
        -- SELECT * FROM app_schema.users LIMIT 1;
    END IF;
END $$;

-- 7. 检查权限
SELECT 
    has_schema_privilege(current_user, 'app_schema', 'USAGE') AS "有USAGE权限",
    has_table_privilege(current_user, 'app_schema.users', 'SELECT') AS "有SELECT权限";
"""
    
    with open('test_table_access.sql', 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print("\n📄 创建了测试脚本: test_table_access.sql")
    print("   使用方法: psql -U 用户名 -d recipe_system -f test_table_access.sql")

def main():
    """主函数"""
    connections = connect_to_database()
    
    try:
        # 对每个成功的连接进行诊断
        for cursor, conn, username in connections:
            print(f"\n\n========= 诊断报告 (用户: {username}) ========\n")
            check_schema_permissions(cursor, username)
            check_table_existence(cursor)
            check_current_search_path(cursor)
            check_case_sensitivity(cursor)
            conn.close()
        
        # 提供通用解决方案
        provide_solutions()
        
        # 创建测试脚本
        create_test_script()
        
    except Exception as e:
        print(f"诊断过程中出错: {e}")
    finally:
        # 确保所有连接都已关闭
        for _, conn, _ in connections:
            try:
                conn.close()
            except:
                pass
        
        print("\n✅ 诊断完成!")

if __name__ == "__main__":
    main()