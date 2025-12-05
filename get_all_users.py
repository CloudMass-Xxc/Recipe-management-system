#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
查询数据库用户表中的所有用户数据
"""

import psycopg2
import os
from dotenv import load_dotenv

def get_all_users():
    """查询数据库中所有用户数据"""
    try:
        # 加载环境变量（如果有.env文件）
        load_dotenv()
        
        # 直接使用数据库连接参数，避免URL中的schema问题
        print("正在连接数据库...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="recipe_system",
            user="app_user",
            password="xxc1018"
        )
        cursor = conn.cursor()
        
        # 设置search_path以包含app_schema
        cursor.execute("SET search_path TO app_schema, public")
        
        # 查询users表中的所有数据
        print("正在查询用户表数据...")
        cursor.execute("SELECT * FROM users")
        
        # 获取列名
        columns = [desc[0] for desc in cursor.description]
        
        # 获取所有用户数据
        users = cursor.fetchall()
        
        # 输出结果
        print(f"\n共找到 {len(users)} 个用户记录：")
        print("-" * 80)
        
        # 输出列名
        print(" | ".join(columns))
        print("-" * 80)
        
        # 输出每条用户数据
        for user in users:
            # 处理可能的None值
            user_data = [str(field) if field is not None else "NULL" for field in user]
            print(" | ".join(user_data))
        
        print("-" * 80)
        
        # 关闭连接
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"查询过程中发生错误: {str(e)}")
        print("\n尝试使用完全限定表名查询...")
        
        # 尝试使用完全限定表名查询
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="recipe_system",
                user="app_user",
                password="xxc1018"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM app_schema.users")
            
            # 获取列名
            columns = [desc[0] for desc in cursor.description]
            
            # 获取所有用户数据
            users = cursor.fetchall()
            
            # 输出结果
            print(f"\n共找到 {len(users)} 个用户记录：")
            print("-" * 80)
            
            # 输出列名
            print(" | ".join(columns))
            print("-" * 80)
            
            # 输出每条用户数据
            for user in users:
                # 处理可能的None值
                user_data = [str(field) if field is not None else "NULL" for field in user]
                print(" | ".join(user_data))
            
            print("-" * 80)
            
            # 关闭连接
            cursor.close()
            conn.close()
            
        except Exception as e2:
            print(f"使用完全限定表名查询时也发生错误: {str(e2)}")

if __name__ == "__main__":
    get_all_users()
