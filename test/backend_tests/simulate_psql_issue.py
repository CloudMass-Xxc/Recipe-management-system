#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PSQL命令模拟工具
用于重现和解决PostgreSQL终端中查询app_schema.users表失败的问题
"""

import os
import subprocess
import time

def run_psql_command(command, db_name=None, username=None, password=None):
    """运行psql命令并返回输出"""
    env = os.environ.copy()
    if password:
        env['PGPASSWORD'] = password
    
    cmd_args = ['psql']
    if username:
        cmd_args.extend(['-U', username])
    if db_name:
        cmd_args.extend(['-d', db_name])
    cmd_args.extend(['-c', command])
    
    try:
        result = subprocess.run(
            cmd_args,
            env=env,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), -1

def main():
    """主函数"""
    print("=== PSQL命令模拟工具 ===")
    print("本工具将模拟用户在psql中遇到的表查询失败问题")
    print("=" * 60)
    
    # 配置信息
    configs = {
        'db_name': 'recipe_system',
        'username': 'app_user',
        'password': 'xxc1018'
    }
    
    print(f"\n📌 使用的配置信息:")
    print(f"   数据库名: {configs['db_name']}")
    print(f"   用户名: {configs['username']}")
    print(f"   主机: localhost")
    print(f"   端口: 5432")
    
    # 测试1: 检查是否连接到了正确的数据库
    print("\n" + "=" * 60)
    print("🔍 测试1: 连接检查")
    print("=" * 60)
    
    # 不指定数据库，连接到默认数据库
    print("\n1. 不指定数据库，连接到默认数据库:")
    stdout, stderr, code = run_psql_command(
        "SELECT current_database(), current_user;",
        username=configs['username'],
        password=configs['password']
    )
    print(f"   输出: {stdout}")
    if stderr:
        print(f"   错误: {stderr}")
    print(f"   返回码: {code}")
    
    # 指定数据库连接
    print("\n2. 指定数据库连接:")
    stdout, stderr, code = run_psql_command(
        "SELECT current_database(), current_user;",
        db_name=configs['db_name'],
        username=configs['username'],
        password=configs['password']
    )
    print(f"   输出: {stdout}")
    if stderr:
        print(f"   错误: {stderr}")
    print(f"   返回码: {code}")
    
    # 测试2: 重现用户遇到的错误
    print("\n" + "=" * 60)
    print("🔍 测试2: 重现用户遇到的错误")
    print("=" * 60)
    
    # 在错误的数据库中查询
    print("\n1. 在默认数据库（可能不是recipe_system）中查询:")
    stdout, stderr, code = run_psql_command(
        "SELECT * FROM app_schema.users;",
        username=configs['username'],
        password=configs['password']
    )
    print(f"   输出: {stdout}")
    if stderr:
        print(f"   错误: {stderr}")
    print(f"   返回码: {code}")
    
    # 在正确的数据库中查询
    print("\n2. 在正确的数据库中查询:")
    stdout, stderr, code = run_psql_command(
        "SELECT * FROM app_schema.users;",
        db_name=configs['db_name'],
        username=configs['username'],
        password=configs['password']
    )
    print(f"   输出: {stdout}")
    if stderr:
        print(f"   错误: {stderr}")
    print(f"   返回码: {code}")
    
    # 测试3: 大小写敏感性测试
    print("\n" + "=" * 60)
    print("🔍 测试3: 大小写敏感性测试")
    print("=" * 60)
    
    # 使用不同大小写查询
    variations = [
        "SELECT * FROM app_schema.users;",
        "SELECT * FROM App_Schema.Users;",
        "SELECT * FROM APP_SCHEMA.USERS;",
        "SELECT * FROM \"app_schema\".\"users\";",
        "SELECT * FROM \"App_Schema\".\"Users\";",
    ]
    
    for i, query in enumerate(variations, 1):
        print(f"\n{i}. 测试查询: {query}")
        stdout, stderr, code = run_psql_command(
            query,
            db_name=configs['db_name'],
            username=configs['username'],
            password=configs['password']
        )
        status = "✅ 成功" if code == 0 else "❌ 失败"
        print(f"   状态: {status}")
        if code != 0 and stderr:
            print(f"   错误: {stderr}")
    
    # 测试4: search_path测试
    print("\n" + "=" * 60)
    print("🔍 测试4: search_path测试")
    print("=" * 60)
    
    # 检查search_path
    print("\n1. 检查当前search_path:")
    stdout, stderr, code = run_psql_command(
        "SHOW search_path;",
        db_name=configs['db_name'],
        username=configs['username'],
        password=configs['password']
    )
    print(f"   当前search_path: {stdout}")
    
    # 设置search_path后查询
    print("\n2. 设置search_path后查询:")
    commands = [
        "SET search_path TO app_schema, public;",
        "SHOW search_path;",
        "SELECT * FROM users;"
    ]
    multi_command = "\\; ".join(commands)
    stdout, stderr, code = run_psql_command(
        multi_command,
        db_name=configs['db_name'],
        username=configs['username'],
        password=configs['password']
    )
    print(f"   输出: {stdout}")
    if stderr:
        print(f"   错误: {stderr}")
    
    # 提供解决方案
    print("\n" + "=" * 60)
    print("💡 解决方案")
    print("=" * 60)
    print("\n根据测试结果，您在psql中查询失败的最可能原因是:")
    print("\n1. 未连接到正确的数据库:")
    print("   ❌ 错误方式: psql -U app_user")
    print("   ✅ 正确方式: psql -U app_user -d recipe_system")
    print("\n2. 或者在连接后切换到正确的数据库:")
    print("   psql -U app_user")
    print("   \\c recipe_system")
    print("\n3. 确保使用正确的表名大小写:")
    print("   ✅ SELECT * FROM app_schema.users;")
    print("   ❌ SELECT * FROM App_Schema.Users;  # 使用了引号的情况除外")
    print("\n4. 设置search_path以简化查询:")
    print("   SET search_path TO app_schema, public;")
    print("   SELECT * FROM users;  # 现在可以直接使用表名")
    
    # 创建一个批处理文件帮助用户快速连接
    print("\n" + "=" * 60)
    print("🚀 快速连接工具")
    print("=" * 60)
    
    # 创建Windows批处理文件
    batch_content = f"@echo off\n"
    batch_content += f"echo 正在连接到PostgreSQL数据库...\n"
    batch_content += f"set PGPASSWORD={configs['password']}\n"
    batch_content += f"psql -U {configs['username']} -d {configs['db_name']} -c \"SET search_path TO app_schema, public; \\dt; SELECT '连接成功!' AS status;\"\n"
    batch_content += f"psql -U {configs['username']} -d {configs['db_name']}\n"
    batch_content += f"pause"
    
    with open("d:\Homework\LLM\Final_assignment\Vers_4\connect_to_db.bat", "w") as f:
        f.write(batch_content)
    
    # 创建SQL脚本文件
    sql_content = "-- 检查连接信息\n"
    sql_content += "SELECT current_database(), current_user;\n\n"
    sql_content += "-- 设置search_path\n"
    sql_content += "SET search_path TO app_schema, public;\n\n"
    sql_content += "-- 列出app_schema中的表\n"
    sql_content += "\\dt app_schema.*\n\n"
    sql_content += "-- 查询users表\n"
    sql_content += "SELECT * FROM app_schema.users;\n\n"
    sql_content += "-- 也可以直接查询\n"
    sql_content += "SELECT * FROM users;"
    
    with open("d:\Homework\LLM\Final_assignment\Vers_4\check_tables.sql", "w") as f:
        f.write(sql_content)
    
    print("\n已创建以下辅助文件:")
    print("1. connect_to_db.bat - Windows批处理文件，双击即可连接到正确的数据库")
    print("2. check_tables.sql - SQL脚本文件，包含检查和查询表的命令")
    print("\n使用方法:")
    print("- Windows用户: 双击 connect_to_db.bat")
    print("- 或运行: psql -U app_user -d recipe_system -f check_tables.sql")
    print("\n✅ 模拟测试完成!")

if __name__ == "__main__":
    main()