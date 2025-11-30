#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试数据库连接和用户表状态的脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, SessionLocal, Base
from app.models.user import User

def test_database_connection():
    """测试数据库连接并查看用户表状态"""
    print('测试数据库连接...')
    
    try:
        # 测试数据库连接
        with engine.connect() as conn:
            print('✅ 数据库连接成功！')
        
        # 测试用户表查询
        db = SessionLocal()
        try:
            # 检查用户表是否存在
            from sqlalchemy import inspect
            inspector = inspect(engine)
            schemas = inspector.get_schema_names()
            print(f'数据库中的schemas: {schemas}')
            
            # 检查表是否存在
            tables = inspector.get_table_names(schema='app_schema')
            print(f'app_schema中的表: {tables}')
            
            # 查询用户数据
            users = db.query(User).all()
            print(f'当前用户表中有 {len(users)} 个用户')
            
            for user in users:
                print(f'用户名: {user.username}, 邮箱: {user.email}, 手机: {user.phone}')
                
        except Exception as e:
            print(f'❌ 查询用户表时出错: {e}')
        finally:
            db.close()
            
    except Exception as e:
        print(f'❌ 数据库连接错误: {e}')

if __name__ == '__main__':
    test_database_connection()
