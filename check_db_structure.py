#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查数据库表结构的脚本
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def check_db_structure():
    """检查数据库表结构"""
    try:
        # 数据库连接参数
        conn_params = {
            'host': 'localhost',
            'port': '5432',
            'user': 'app_user',
            'password': 'xxc1018',
            'dbname': 'recipe_system'
        }
        
        print("正在连接数据库...")
        # 连接数据库
        conn = psycopg2.connect(**conn_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # 创建游标
        cursor = conn.cursor()
        
        print("\n=== 检查users表的字段 ===")
        cursor.execute("""
        SELECT column_name, data_type, is_nullable 
        FROM information_schema.columns 
        WHERE table_name = 'users'
        ORDER BY ordinal_position;
        """)
        
        print("\nusers表的字段信息：")
        print("-" * 60)
        print(f"{'字段名':<20} {'数据类型':<20} {'是否可空':<10}")
        print("-" * 60)
        for row in cursor.fetchall():
            print(f"{row[0]:<20} {row[1]:<20} {row[2]:<10}")
        print("-" * 60)
        
        # 尝试查询一条记录（如果存在）
        print("\n=== 尝试查询users表的记录 ===")
        try:
            cursor.execute("SELECT * FROM users LIMIT 1")
            columns = [desc[0] for desc in cursor.description]
            print(f"\n查询成功！表中包含的字段：{columns}")
            
            row = cursor.fetchone()
            if row:
                print(f"\n示例记录：{dict(zip(columns, row))}")
            else:
                print("\n表中没有记录。")
        except Exception as e:
            print(f"\n查询记录时出错：{e}")
        
        # 检查schema设置
        print("\n=== 检查数据库schema设置 ===")
        try:
            cursor.execute("SHOW search_path")
            search_path = cursor.fetchone()[0]
            print(f"当前的search_path: {search_path}")
            
            # 检查是否存在app_schema
            cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name = 'app_schema';
            """)
            if cursor.fetchone():
                print("app_schema 存在")
                
                # 检查app_schema中是否有users表
                cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_schema = 'app_schema' AND table_name = 'users'
                ORDER BY ordinal_position;
                """)
                if cursor.fetchall():
                    print("\napp_schema.users表存在！")
                else:
                    print("\napp_schema.users表不存在")
            else:
                print("app_schema 不存在")
                
        except Exception as e:
            print(f"\n检查schema时出错：{e}")
        
        # 关闭游标和连接
        cursor.close()
        conn.close()
        
        print("\n数据库检查完成！")
        
    except Exception as e:
        print(f"连接数据库时发生错误：{e}")

if __name__ == "__main__":
    print("开始执行数据库结构检查脚本...")
    check_db_structure()
