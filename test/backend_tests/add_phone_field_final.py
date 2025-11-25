#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
添加phone字段到users表的最终版Python脚本
确保使用正确的数据库连接信息和schema
"""

import os
import sys
import psycopg2

def add_phone_field():
    """检查并添加phone字段到public schema的users表"""
    print("=== 开始添加phone字段到users表 ===")
    
    # 使用正确的数据库连接信息
    # 从用户提供的信息和之前的成功经验中获取
    user = 'app_user'
    password = 'xxc1018'  # 正确的密码
    host = 'localhost'
    port = '5432'
    dbname = 'recipe_system'
    schema_name = 'public'  # 明确指定schema
    
    print(f"数据库连接信息: {user}@{host}:{port}/{dbname}")
    print(f"目标schema: {schema_name}")
    
    try:
        # 连接数据库
        print("正在连接数据库...")
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True  # 启用自动提交
        cursor = conn.cursor()
        print("✅ 数据库连接成功!")
        
        # 明确设置search_path到public
        cursor.execute("SET search_path TO public")
        print(f"已将search_path设置为{schema_name}")
        
        # 检查users表是否存在于任何schema中
        try:
            print(f"检查所有schema中是否存在users表...")
            
            # 查找所有schema中的users表
            cursor.execute(
                "SELECT table_schema, table_name FROM information_schema.tables WHERE table_name='users'"
            )
            found_tables = cursor.fetchall()
            
            if not found_tables:
                print(f"❌ 错误: 在数据库中找不到名为'users'的表")
                # 列出所有schema和表，以便找出正确的表名
                print("\n📋 列出数据库中的所有schema和表:")
                cursor.execute(
                    "SELECT table_schema, table_name FROM information_schema.tables ORDER BY table_schema, table_name"
                )
                all_tables = cursor.fetchall()
                if all_tables:
                    print("找到以下表:")
                    for schema, table in all_tables:
                        print(f"- {schema}.{table}")
                else:
                    print("在数据库中没有找到任何表")
                cursor.close()
                conn.close()
                return False
            else:
                # 使用找到的第一个匹配的表
                actual_schema, actual_table = found_tables[0]
                print(f"✅ 找到users表: {actual_schema}.{actual_table}")
                # 更新schema_name为实际找到的schema
                schema_name = actual_schema
        except Exception as e:
            print(f"❌ 检查users表时出错: {e}")
            cursor.close()
            conn.close()
            return False
        
        # 检查phone字段是否已存在
        print("检查phone字段是否已存在...")
        cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema=%s AND table_name='users' AND column_name='phone'",
            (schema_name,)
        )
        
        if not cursor.fetchone():
            print(f"添加phone字段到{schema_name}.users表...")
            # 添加phone字段，设置为唯一且可为空
            cursor.execute(
                "ALTER TABLE users ADD COLUMN phone VARCHAR(20) UNIQUE NULL"
            )
            print("✅ phone字段添加成功!")
            
            # 为phone字段创建索引
            print("为phone字段创建索引...")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone)")
            print("✅ 索引创建成功!")
        else:
            print(f"ℹ️ phone字段已存在于{schema_name}.users表中")
        
        # 验证字段添加结果
        print("\n📋 验证字段添加结果:")
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
            print("❌ 未找到添加的phone字段")
            success = False
        
        # 显示users表的完整结构
        print("\n📊 users表当前结构:")
        cursor.execute(
            "SELECT column_name, data_type, character_maximum_length, is_nullable "
            "FROM information_schema.columns "
            "WHERE table_schema=%s AND table_name='users' "
            "ORDER BY ordinal_position",
            (schema_name,)
        )
        
        print("-" * 80)
        print(f"{'列名':<20} {'数据类型':<20} {'最大长度':<10} {'可为空':<10}")
        print("-" * 80)
        
        for row in cursor.fetchall():
            col_name = row[0]
            data_type = row[1]
            max_len = str(row[2]) if row[2] is not None else 'N/A'
            nullable = '是' if row[3] == 'YES' else '否'
            print(f"{col_name:<20} {data_type:<20} {max_len:<10} {nullable:<10}")
        
        print("-" * 80)
        
        cursor.close()
        conn.close()
        return success
        
    except psycopg2.OperationalError as e:
        print(f"❌ 数据库操作错误: {e}")
        print("请检查数据库连接信息和权限")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    success = add_phone_field()
    if success:
        print("\n🎉 操作完成! phone字段已成功添加到users表")
        return 0
    else:
        print("\n❌ 操作失败!请检查错误信息并重新尝试")
        return 1

if __name__ == "__main__":
    sys.exit(main())