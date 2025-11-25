#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
添加phone字段到users表的Python脚本
使用项目中正确的数据库配置
"""

import os
import re
import sys
import psycopg2
from dotenv import load_dotenv

# 确保脚本可以找到项目模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

def add_phone_field():
    """检查并添加phone字段到users表"""
    print("开始添加phone字段到users表...")
    
    # 加载环境变量
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        print(f"已从 {dotenv_path} 加载环境变量")
    else:
        print(f"警告: 未找到 .env 文件在 {dotenv_path}")
    
    # 使用正确的数据库连接信息
    print("使用正确的数据库连接信息...")
    user = 'app_user'
    password = 'xxc1018'  # 从backend/.env文件中获取的正确密码
    host = 'localhost'
    port = '5432'
    dbname = 'recipe_system'
    print(f"解析连接信息: user={user}, host={host}, port={port}, dbname={dbname}")
    
    try:
        
        # 尝试连接数据库
        print("正在连接数据库...")
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("数据库连接成功!")
        
        # 检查是否存在public schema中的users表
        cursor.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='users'"
        )
        if cursor.fetchone():
            print("在public schema中找到users表")
            schema_name = 'public'
        else:
            # 检查是否存在其他schema中的users表
            cursor.execute(
                "SELECT table_schema FROM information_schema.tables WHERE table_name='users'"
            )
            schemas = cursor.fetchall()
            if schemas:
                schema_name = schemas[0][0]
                print(f"在{schema_name} schema中找到users表")
                cursor.execute(f"SET search_path TO {schema_name}")
            else:
                print("错误: 找不到users表")
                cursor.close()
                conn.close()
                return False
        
        # 检查phone字段是否存在
        print("检查phone字段是否已存在...")
        cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema=%s AND table_name='users' AND column_name='phone'",
            (schema_name,)
        )
        
        if not cursor.fetchone():
            print(f"在{schema_name}.users表中添加phone字段...")
            # 添加phone字段，设置为唯一且可为空
            cursor.execute(
                "ALTER TABLE users ADD COLUMN phone VARCHAR(20) UNIQUE NULL"
            )
            print(f"phone字段添加成功! 在{schema_name}.users表中")
            
            # 为phone字段创建索引
            print("为phone字段创建索引...")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone)")
            print("索引创建成功!")
        else:
            print(f"phone字段已存在于{schema_name}.users表中，跳过添加操作")
        
        # 验证字段是否添加成功
        print("\n验证字段添加结果:")
        cursor.execute(
            "SELECT column_name, data_type, character_maximum_length, is_nullable "
            "FROM information_schema.columns "
            "WHERE table_schema=%s AND table_name='users' AND column_name='phone'",
            (schema_name,)
        )
        result = cursor.fetchone()
        if result:
            print(f"字段名称: {result[0]}")
            print(f"数据类型: {result[1]}")
            print(f"最大长度: {result[2]}")
            print(f"是否可为空: {result[3]}")
            success = True
        else:
            print("警告: 未找到添加的phone字段")
            success = False
        
        cursor.close()
        conn.close()
        return success
        
    except psycopg2.OperationalError as e:
        print(f"数据库操作错误: {e}")
        print("请检查数据库连接信息和权限")
        return False
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=== phone字段添加工具 ===")
    success = add_phone_field()
    if success:
        print("\n✅ 操作完成!")
        return 0
    else:
        print("\n❌ 操作失败!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
