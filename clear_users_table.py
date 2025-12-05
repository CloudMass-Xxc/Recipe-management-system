#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理数据库用户表数据脚本

此脚本用于清空recipe_system数据库中的用户表数据，
同时处理相关的外键关系，确保数据完整性。
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def get_db_connection_string():
    """
    获取数据库连接字符串
    """
    return "postgresql://app_user:xxc1018@localhost:5432/recipe_system"

def clear_users_table():
    """
    清空用户表及其相关依赖表的数据
    """
    print("开始清理用户表数据...")
    
    db_url = get_db_connection_string()
    print(f"使用数据库连接: {db_url}")
    
    try:
        # 创建数据库引擎
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            # 开始事务
            transaction = connection.begin()
            
            try:
                # 设置搜索路径到app_schema
                connection.execute(text("SET search_path TO app_schema, public"))
                print("已设置搜索路径到app_schema")
                
                # 按依赖关系顺序删除数据
                print("\n按依赖关系顺序删除数据...")
                
                # 定义删除顺序（从最依赖到最少依赖）
                tables_to_clear = [
                    # 依赖users表的子表
                    "meal_plan_recipes",  # 依赖meal_plans
                    "meal_plans",         # 依赖users
                    "diet_plans",         # 依赖users
                    "recipe_ingredients",  # 依赖recipes
                    "favorites",          # 依赖users和recipes
                    "ratings",            # 依赖users和recipes
                    "user_recipe_interactions",  # 依赖users和recipes
                    "recipes",            # 可能有其他表依赖
                    "tokens",             # 依赖users
                    "security_logs",      # 依赖users
                    "users"               # 用户表（最后删除）
                ]
                
                # 执行删除操作
                for table_name in tables_to_clear:
                    try:
                        # 检查表是否存在
                        check_table_query = text("""
                            SELECT EXISTS (
                                SELECT FROM information_schema.tables 
                                WHERE table_schema = 'app_schema' 
                                AND table_name = :table_name
                            )
                        """)
                        table_exists = connection.execute(
                            check_table_query, 
                            {"table_name": table_name}
                        ).scalar()
                        
                        if table_exists:
                            # 获取删除前的记录数
                            count_query = text(f"SELECT COUNT(*) FROM {table_name}")
                            before_count = connection.execute(count_query).scalar()
                            
                            if before_count > 0:
                                # 执行删除操作
                                delete_query = text(f"DELETE FROM {table_name}")
                                result = connection.execute(delete_query)
                                
                                print(f"  ✓ 已清空 {table_name} 表: {before_count} 条记录")
                            else:
                                print(f"  ✓ {table_name} 表为空，跳过")
                        else:
                            print(f"  ! 未找到 {table_name} 表，跳过")
                    except SQLAlchemyError as e:
                        print(f"  ✗ 清空 {table_name} 表时出错: {e}")
                        raise
                
                # 提交事务
                transaction.commit()
                print("\n✅ 所有表数据清理完成！")
                
            except Exception as e:
                # 回滚事务
                transaction.rollback()
                print(f"\n❌ 清理过程中发生错误，事务已回滚: {e}")
                return False
    
    except SQLAlchemyError as e:
        print(f"❌ 数据库连接错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")
        return False
    
    return True

def verify_cleanup():
    """
    验证清理结果
    """
    print("\n验证清理结果...")
    
    db_url = get_db_connection_string()
    
    try:
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            # 设置搜索路径
            connection.execute(text("SET search_path TO app_schema, public"))
            
            # 检查关键表的记录数
            tables_to_check = ["users", "recipes", "tokens", "favorites"]
            
            for table_name in tables_to_check:
                try:
                    count_query = text(f"SELECT COUNT(*) FROM {table_name}")
                    count = connection.execute(count_query).scalar()
                    print(f"  {table_name} 表记录数: {count}")
                except Exception as e:
                    print(f"  ! 检查 {table_name} 表时出错: {e}")
    
    except Exception as e:
        print(f"❌ 验证过程中发生错误: {e}")

def main():
    """
    主函数
    """
    print("=======================================================")
    print("        数据库用户表数据清理工具")
    print("=======================================================")
    print("此工具将清空recipe_system数据库中的用户表数据，")
    print("同时处理相关的外键关系，确保数据完整性。")
    print("=======================================================")
    
    # 检查是否有自动确认参数
    auto_confirm = len(sys.argv) > 1 and sys.argv[1] == '--yes'
    
    if not auto_confirm:
        # 提示用户确认
        confirm = input("\n确认要清空所有用户数据吗？(y/n): ").lower()
        if confirm != 'y':
            print("操作已取消。")
            return
    else:
        print("\n使用自动确认模式，跳过用户交互。")
    
    # 执行清理操作
    success = clear_users_table()
    
    # 验证清理结果
    if success:
        verify_cleanup()
    
    print("\n=======================================================")
    print("操作完成！")
    print("=======================================================")

if __name__ == "__main__":
    print(f"运行参数: {sys.argv[1:]}")
    main()
