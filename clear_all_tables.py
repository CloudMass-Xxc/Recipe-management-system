#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清空数据库中所有表的数据脚本

此脚本会安全地清空PostgreSQL数据库中app_schema模式下所有表的数据，
考虑外键约束，按照正确的顺序执行清空操作。
"""

import psycopg2
import psycopg2.extensions
from psycopg2.errors import ForeignKeyViolation

# 数据库连接信息
db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'recipe_system',
    'user': 'app_user',
    'password': 'xxc1018'
}

def get_all_tables(cursor):
    """获取app_schema下的所有表名"""
    print("\n🔍 获取app_schema下的所有表...")
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'app_schema' 
        AND table_type = 'BASE TABLE'
    """)
    tables = [table[0] for table in cursor.fetchall()]
    print(f"✅ 找到 {len(tables)} 个表: {', '.join(tables)}")
    return tables

def get_table_dependencies(cursor):
    """获取表之间的外键依赖关系"""
    print("\n🔍 获取表之间的外键依赖关系...")
    cursor.execute("""
        SELECT 
            tc.table_name AS referencing_table,
            ccu.table_name AS referenced_table
        FROM 
            information_schema.table_constraints AS tc
        JOIN 
            information_schema.constraint_column_usage AS ccu
        ON 
            tc.constraint_name = ccu.constraint_name
        WHERE 
            tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_schema = 'app_schema'
            AND ccu.table_schema = 'app_schema'
    """)
    
    dependencies = {}
    for referencing, referenced in cursor.fetchall():
        if referencing not in dependencies:
            dependencies[referencing] = []
        dependencies[referencing].append(referenced)
    
    print("✅ 外键依赖关系:")
    for ref_table, deps in dependencies.items():
        print(f"   {ref_table} -> {', '.join(deps)}")
    
    return dependencies

def topological_sort(tables, dependencies):
    """对表进行拓扑排序，确保先删除没有依赖的表"""
    print("\n🔍 对表进行拓扑排序...")
    
    # 创建依赖计数和邻接表
    in_degree = {table: 0 for table in tables}
    adjacency = {table: [] for table in tables}
    
    # 计算每个表的入度（被多少表引用）
    for referencing, referenced_list in dependencies.items():
        for referenced in referenced_list:
            if referenced in tables and referencing in tables:
                adjacency[referenced].append(referencing)
                in_degree[referencing] += 1
    
    # 找出所有入度为0的表（没有被其他表引用）
    queue = [table for table, degree in in_degree.items() if degree == 0]
    sorted_tables = []
    
    # 拓扑排序
    while queue:
        current = queue.pop(0)
        sorted_tables.append(current)
        
        for neighbor in adjacency[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # 添加可能的循环依赖表（如果有）
    for table in tables:
        if table not in sorted_tables:
            sorted_tables.append(table)
    
    # 反转排序结果，确保先删除引用表，再删除被引用表
    sorted_tables.reverse()
    
    print(f"✅ 排序结果: {', '.join(sorted_tables)}")
    return sorted_tables

def truncate_all_tables(cursor, sorted_tables):
    """按照排序顺序清空所有表的数据"""
    print("\n🔍 开始清空表数据...")
    
    # 先禁用外键检查（注意：在生产环境中要谨慎使用）
    try:
        cursor.execute("SET CONSTRAINTS ALL DEFERRED")
        print("✅ 已禁用外键约束检查")
    except Exception as e:
        print(f"⚠️  禁用外键约束检查失败: {e}")
    
    # 清空每个表
    success_count = 0
    failure_count = 0
    
    for table in sorted_tables:
        try:
            # 使用TRUNCATE命令清空表，比DELETE更高效
            cursor.execute(f"TRUNCATE TABLE app_schema.{table} CASCADE")
            print(f"✅ 成功清空表: {table}")
            success_count += 1
        except Exception as e:
            print(f"❌ 清空表 {table} 失败: {e}")
            # 如果TRUNCATE失败，尝试使用DELETE
            try:
                cursor.execute(f"DELETE FROM app_schema.{table}")
                print(f"✅ 成功使用DELETE清空表: {table}")
                success_count += 1
            except Exception as e2:
                print(f"❌ DELETE表 {table} 也失败: {e2}")
                failure_count += 1
    
    print(f"\n📊 清空结果:")
    print(f"   成功: {success_count}")
    print(f"   失败: {failure_count}")
    
    return success_count, failure_count

def verify_tables_emptied(cursor, tables):
    """验证所有表是否已清空"""
    print("\n🔍 验证表是否已清空...")
    
    empty_tables = []
    non_empty_tables = []
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM app_schema.{table}")
            count = cursor.fetchone()[0]
            
            if count == 0:
                empty_tables.append(table)
                print(f"✅ {table}: 已清空 (0 条记录)")
            else:
                non_empty_tables.append((table, count))
                print(f"❌ {table}: 仍有 {count} 条记录")
        except Exception as e:
            print(f"⚠️  验证表 {table} 时出错: {e}")
    
    print(f"\n📊 验证结果:")
    print(f"   已清空: {len(empty_tables)}")
    print(f"   未清空: {len(non_empty_tables)}")
    
    if non_empty_tables:
        print("\n❌ 以下表仍有数据:")
        for table, count in non_empty_tables:
            print(f"   - {table}: {count} 条记录")
    
    return len(empty_tables) == len(tables)

def main():
    """主函数"""
    print("=== 数据库清空工具 ===")
    print("此工具将清空recipe_system数据库中app_schema下所有表的数据")
    print("=" * 50)
    
    # 连接到数据库
    conn = None
    cursor = None
    
    try:
        print("\n🔍 连接到数据库...")
        conn = psycopg2.connect(**db_params)
        conn.autocommit = False  # 禁用自动提交，使用事务
        cursor = conn.cursor()
        print("✅ 数据库连接成功!")
        
        # 获取所有表
        tables = get_all_tables(cursor)
        
        if not tables:
            print("\n⚠️  未找到任何表，操作中止")
            return
        
        # 获取表依赖关系
        dependencies = get_table_dependencies(cursor)
        
        # 拓扑排序
        sorted_tables = topological_sort(tables, dependencies)
        
        # 确认操作
        print("\n⚠️  警告：此操作将清空以下表的所有数据：")
        print(f"   {', '.join(sorted_tables)}")
        confirm = input("\n确认要清空所有表数据吗？(y/N): ")
        
        if confirm.lower() != 'y':
            print("\n✅ 操作已取消")
            return
        
        # 清空所有表
        print("\n🚀 开始执行清空操作...")
        success_count, failure_count = truncate_all_tables(cursor, sorted_tables)
        
        # 提交事务
        conn.commit()
        print("\n✅ 事务已提交")
        
        # 验证结果
        all_empty = verify_tables_emptied(cursor, tables)
        
        if all_empty:
            print("\n🎉 所有表已成功清空!")
        else:
            print("\n⚠️  部分表未能清空，请检查错误信息")
        
    except Exception as e:
        print(f"\n❌ 操作过程中发生错误: {e}")
        # 回滚事务
        if conn:
            try:
                conn.rollback()
                print("✅ 事务已回滚")
            except Exception as rollback_e:
                print(f"❌ 事务回滚失败: {rollback_e}")
    finally:
        # 关闭连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("\n✅ 数据库连接已关闭")

if __name__ == "__main__":
    main()
