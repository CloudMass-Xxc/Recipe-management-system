#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清空用户数据的Python脚本
使用psycopg2连接数据库并尝试清空用户数据
"""

import psycopg2
from psycopg2 import OperationalError
import os

# 数据库连接参数
DB_HOST = "localhost"
DB_DATABASE = "recipe_system"
DB_USER = "app_user"
DB_PASSWORD = "xxc1018"  # 用户提供的密码


def connect_to_db():
    """连接到PostgreSQL数据库"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_DATABASE,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("成功连接到数据库")
        return conn
    except OperationalError as e:
        print(f"连接数据库失败: {e}")
        return None


def clear_user_data(conn):
    """尝试清空用户数据"""
    try:
        cursor = conn.cursor()
        
        # 先尝试查看有多少用户
        print("\n尝试查看当前用户数量...")
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"当前用户数量: {count}")
        except Exception as e:
            print(f"查看用户数量失败: {e}")
        
        # 尝试删除用户数据
        print("\n尝试删除用户数据...")
        try:
            # 由于可能存在外键约束，我们需要先处理相关表
            cursor.execute("DELETE FROM diet_plans WHERE user_id IN (SELECT user_id FROM users)")
            cursor.execute("DELETE FROM favorites WHERE user_id IN (SELECT user_id FROM users)")
            cursor.execute("DELETE FROM ratings WHERE user_id IN (SELECT user_id FROM users)")
            
            # 然后删除用户数据
            cursor.execute("DELETE FROM users")
            
            conn.commit()
            print("用户数据已成功删除")
            
            # 验证删除结果
            cursor.execute("SELECT COUNT(*) FROM users")
            count_after = cursor.fetchone()[0]
            print(f"删除后用户数量: {count_after}")
            
        except Exception as e:
            print(f"删除用户数据失败: {e}")
            conn.rollback()
        
        cursor.close()
    except Exception as e:
        print(f"执行操作时出错: {e}")


def main():
    """主函数"""
    print("开始清空用户数据...")
    conn = connect_to_db()
    if conn:
        try:
            clear_user_data(conn)
        finally:
            conn.close()
            print("\n数据库连接已关闭")


if __name__ == "__main__":
    main()
