#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
检查数据库中的用户信息，用于调试登录问题
"""

import sys
import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('check_user_script')

# 加载环境变量
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def check_user_in_db(username=None, email=None, phone=None):
    """检查数据库中是否存在指定用户"""
    try:
        # 获取数据库连接字符串
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            logger.error("DATABASE_URL 环境变量未设置")
            return False
        
        logger.info(f"连接到数据库: {db_url}")
        
        # 创建数据库引擎和会话
        engine = create_engine(db_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # 构建查询条件
            conditions = []
            params = {}
            
            if username:
                conditions.append("username = :username")
                params["username"] = username
            if email:
                conditions.append("email = :email")
                params["email"] = email
            if phone:
                conditions.append("phone = :phone")
                params["phone"] = phone
            
            if not conditions:
                logger.error("至少需要提供username、email或phone之一")
                return False
            
            # 构建查询SQL
            query = f"SELECT * FROM users WHERE {' OR '.join(conditions)}"
            logger.info(f"执行查询: {query}")
            logger.info(f"查询参数: {params}")
            
            # 执行查询
            result = db.execute(text(query), params)
            users = result.fetchall()
            
            # 打印结果
            if users:
                logger.info(f"找到 {len(users)} 个用户")
                for user in users:
                    user_dict = dict(user._mapping)
                    logger.info(f"用户信息: {user_dict}")
                    return True
            else:
                logger.warning("未找到匹配的用户")
                return False
                
        finally:
            db.close()
            engine.dispose()
            
    except Exception as e:
        logger.error(f"检查用户时发生错误: {e}", exc_info=True)
        return False

def main():
    """主函数"""
    logger.info("开始检查用户信息...")
    
    # 检查特定用户（从前端登录尝试中看到的）
    logger.info("\n=== 检查用户: xxiaochang@qq.com ===")
    check_user_in_db(email="xxiaochang@qq.com")
    
    logger.info("\n=== 检查用户: 13160697108 ===")
    check_user_in_db(phone="13160697108")
    
    # 检查所有用户
    logger.info("\n=== 检查所有用户 ===")
    try:
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            logger.error("DATABASE_URL 环境变量未设置")
            return
        
        engine = create_engine(db_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            result = db.execute(text("SELECT username, email, phone, is_active, created_at FROM users"))
            users = result.fetchall()
            
            logger.info(f"数据库中共有 {len(users)} 个用户")
            for user in users:
                user_dict = dict(user._mapping)
                logger.info(f"用户: {user_dict}")
                
        finally:
            db.close()
            engine.dispose()
            
    except Exception as e:
        logger.error(f"检查所有用户时发生错误: {e}", exc_info=True)
    
    logger.info("检查完成")

if __name__ == "__main__":
    main()
