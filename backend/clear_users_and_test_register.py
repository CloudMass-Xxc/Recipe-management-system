#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清空用户表数据并测试注册功能的脚本
"""

import sys
import os
import requests
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.recipe import Recipe  # 导入Recipe模型以处理外键约束
from app.models.favorite import Favorite  # 导入Favorite模型
from app.models.rating import Rating  # 导入Rating模型
from app.models.diet_plan import DietPlan  # 导入DietPlan模型

def clear_users_data():
    """清空用户表数据"""
    print('\n开始清空用户数据...')
    
    db = SessionLocal()
    try:
        # 先删除依赖用户的记录（处理外键约束）
        print('1. 删除收藏记录...')
        db.query(Favorite).delete()
        
        print('2. 删除评分记录...')
        db.query(Rating).delete()
        
        print('3. 删除饮食计划...')
        db.query(DietPlan).delete()
        
        print('4. 删除用户创建的食谱...')
        db.query(Recipe).delete()
        
        print('5. 删除用户记录...')
        user_count = db.query(User).delete()
        
        db.commit()
        print(f'✅ 成功清空 {user_count} 个用户记录及相关数据')
        
        # 验证清空结果
        remaining_users = db.query(User).count()
        print(f'当前用户表中剩余用户数: {remaining_users}')
        
    except Exception as e:
        print(f'❌ 清空数据时出错: {e}')
        db.rollback()
    finally:
        db.close()

def test_register_function():
    """测试注册功能"""
    print('\n开始测试注册功能...')
    
    # 注册API的URL
    register_url = "http://localhost:8001/auth/register"
    
    # 测试注册数据
    test_user = {
        "username": "test_user_new",
        "email": "test_user_new@example.com",
        "phone": "13900139000",
        "password": "TestPassword123",
        "display_name": "测试用户"
    }
    
    print(f'注册数据: {json.dumps(test_user, ensure_ascii=False)}')
    print(f'注册API URL: {register_url}')
    
    try:
        # 发送注册请求
        response = requests.post(
            register_url,
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f'响应状态码: {response.status_code}')
        print(f'响应内容: {response.text}')
        
        if response.status_code == 201:
            print('✅ 注册成功！')
            return True
        else:
            print('❌ 注册失败')
            return False
            
    except Exception as e:
        print(f'❌ 请求异常: {e}')
        return False

def verify_user_in_database():
    """验证用户是否成功保存到数据库"""
    print('\n验证用户是否成功保存到数据库...')
    
    db = SessionLocal()
    try:
        # 查询刚才注册的用户
        user = db.query(User).filter(User.username == "test_user_new").first()
        
        if user:
            print('✅ 用户成功保存到数据库！')
            print(f'用户信息:')
            print(f'  username: {user.username}')
            print(f'  email: {user.email}')
            print(f'  phone: {user.phone}')
            print(f'  display_name: {user.display_name}')
            print(f'  created_at: {user.created_at}')
            return True
        else:
            print('❌ 用户未保存到数据库')
            return False
            
    except Exception as e:
        print(f'❌ 验证过程中出错: {e}')
        return False
    finally:
        db.close()

if __name__ == '__main__':
    print('=' * 60)
    print(f'{"清空用户数据并测试注册功能":^58}')
    print('=' * 60)
    
    # 1. 清空用户数据
    clear_users_data()
    
    # 2. 测试注册功能
    register_success = test_register_function()
    
    # 3. 验证用户是否成功保存到数据库
    if register_success:
        verify_user_in_database()
    
    print('\n测试完成！')
