#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证PostgreSQL表访问
简化版脚本来直接测试app_schema.users表的访问
"""

import psycopg2

def main():
    """主函数"""
    print("=== 表访问验证工具 ===")
    
    try:
        # 连接配置
        conn_params = {
            'dbname': 'recipe_system',
            'user': 'app_user',
            'password': 'xxc1018',
            'host': 'localhost',
            'port': '5432'
        }
        
        print("\n1. 连接到数据库...")
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cursor = conn.cursor()
        print("✅ 连接成功!")
        
        # 测试1: 使用完全限定名查询
        print("\n2. 测试使用完全限定名查询表:")
        try:
            cursor.execute("SELECT COUNT(*) FROM app_schema.users")
            count = cursor.fetchone()[0]
            print(f"✅ 成功查询: app_schema.users 表中有 {count} 条记录")
            print("   这证明表存在且可以被访问")
        except Exception as e:
            print(f"❌ 查询失败: {e}")
        
        # 测试2: 检查当前search_path
        print("\n3. 检查当前search_path:")
        cursor.execute("SHOW search_path")
        search_path = cursor.fetchone()[0]
        print(f"当前search_path: {search_path}")
        
        # 测试3: 设置search_path后再查询
        print("\n4. 设置search_path后再测试:")
        cursor.execute("SET search_path TO app_schema, public")
        print("✅ 已设置 search_path TO app_schema, public")
        
        cursor.execute("SHOW search_path")
        new_search_path = cursor.fetchone()[0]
        print(f"新的search_path: {new_search_path}")
        
        # 测试4: 不使用schema前缀查询
        print("\n5. 不使用schema前缀直接查询:")
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"✅ 成功查询: users 表中有 {count} 条记录")
            print("   这证明search_path设置有效")
        except Exception as e:
            print(f"❌ 查询失败: {e}")
        
        # 测试5: 列出所有表以确认表名
        print("\n6. 列出app_schema中的所有表:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'app_schema'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        print(f"找到 {len(tables)} 个表:")
        for (table,) in tables:
            print(f"   - {table}")
        
        # 测试6: 检查psql命令示例
        print("\n7. psql命令示例:")
        print("   方法1: 设置search_path后查询")
        print("      psql -U app_user -d recipe_system")
        print("      SET search_path TO app_schema, public;")
        print("      SELECT * FROM users;")
        print("   ")
        print("   方法2: 使用完全限定名")
        print("      psql -U app_user -d recipe_system")
        print("      SELECT * FROM app_schema.users;")
        
    except Exception as e:
        print(f"连接失败: {e}")
    finally:
        try:
            conn.close()
        except:
            pass
        
        print("\n✅ 验证完成!")

if __name__ == "__main__":
    main()