#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
添加缺失的display_name字段到users表
"""

import os
import sys
from sqlalchemy import create_engine, text

# 直接使用固定的数据库连接字符串
DATABASE_URL = "postgresql://app_user:xxc1018@localhost:5432/recipe_system"

def add_display_name_column():
    """添加display_name字段到users表"""
    try:
        # 创建数据库引擎
        engine = create_engine(DATABASE_URL)
        
        # 连接数据库
        with engine.connect() as conn:
            print("正在连接数据库...")
            
            # 开始事务
            trans = conn.begin()
            try:
                # 检查并添加display_name字段
                print("检查并添加display_name字段...")
                conn.execute(text("""
                DO $$ 
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_name = 'users' AND column_name = 'display_name'
                    ) THEN
                        ALTER TABLE users ADD COLUMN display_name character varying(255);
                        RAISE NOTICE '已添加display_name字段';
                    ELSE
                        RAISE NOTICE 'display_name字段已存在';
                    END IF;
                END $$;
                """))
                
                # 提交事务
                trans.commit()
                print("事务提交成功")
                
                # 验证字段是否添加成功
                print("验证字段是否添加成功...")
                result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'users'
                ORDER BY ordinal_position;
                """))
                
                print("\nusers表的字段信息：")
                print("-" * 40)
                print(f"{'字段名':<25} {'数据类型':<15}")
                print("-" * 40)
                for row in result:
                    print(f"{row[0]:<25} {row[1]:<15}")
                print("-" * 40)
                
            except Exception as e:
                # 回滚事务
                trans.rollback()
                print(f"事务回滚：{e}")
                return False
        
        print("\ndisplay_name字段添加成功！")
        return True
        
    except Exception as e:
        print(f"添加字段时发生错误：{e}")
        return False

if __name__ == "__main__":
    print("开始执行添加display_name字段的脚本...")
    success = add_display_name_column()
    if success:
        print("脚本执行成功！")
        sys.exit(0)
    else:
        print("脚本执行失败！")
        sys.exit(1)
