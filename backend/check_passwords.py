#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
检查用户密码哈希值和验证逻辑
"""

import os
import sys
import logging
from app.models.user import User
from app.core.database import SessionLocal
from app.auth.password import get_password_hash, verify_password

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('check_password_script')

def check_user_passwords():
    """检查数据库中用户的密码哈希值"""
    try:
        # 创建数据库连接
        db = SessionLocal()
        
        try:
            # 查询所有用户
            users = db.query(User).all()
            logger.info(f"找到 {len(users)} 个用户")
            
            for user in users:
                logger.info(f"\n=== 用户信息 ===")
                logger.info(f"用户ID: {user.user_id}")
                logger.info(f"用户名: {user.username}")
                logger.info(f"邮箱: {user.email}")
                logger.info(f"手机号: {user.phone}")
                logger.info(f"密码哈希: {user.password_hash}")
                logger.info(f"密码哈希长度: {len(user.password_hash)}")
                logger.info(f"密码哈希前10个字符: {user.password_hash[:10]}")
                
                # 测试密码验证
                test_passwords = ["password123", "test123", "admin123"]
                for test_pass in test_passwords:
                    result = verify_password(test_pass, user.password_hash)
                    logger.info(f"验证密码 '{test_pass}': {'✅ 正确' if result else '❌ 错误'}")
                
                # 生成新的哈希值进行对比
                new_hash = get_password_hash("password123")
                logger.info(f"\n=== 新生成的哈希值对比 ===")
                logger.info(f"新哈希值: {new_hash}")
                logger.info(f"新哈希值长度: {len(new_hash)}")
                logger.info(f"新哈希值前10个字符: {new_hash[:10]}")
                
                # 验证新生成的哈希值
                result = verify_password("password123", new_hash)
                logger.info(f"验证新哈希值: {'✅ 正确' if result else '❌ 错误'}")
                
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"检查密码时发生错误: {e}", exc_info=True)

def test_password_functions():
    """测试密码函数的基本功能"""
    try:
        logger.info("\n=== 测试密码函数 ===")
        
        # 测试密码哈希生成
        test_password = "password123"
        hash1 = get_password_hash(test_password)
        hash2 = get_password_hash(test_password)
        
        logger.info(f"原始密码: {test_password}")
        logger.info(f"哈希值1: {hash1}")
        logger.info(f"哈希值2: {hash2}")
        logger.info(f"两次哈希是否相同: {hash1 == hash2}")
        
        # 测试密码验证
        result1 = verify_password(test_password, hash1)
        result2 = verify_password(test_password, hash2)
        result3 = verify_password("wrong_password", hash1)
        
        logger.info(f"验证正确密码 (哈希1): {'✅ 正确' if result1 else '❌ 错误'}")
        logger.info(f"验证正确密码 (哈希2): {'✅ 正确' if result2 else '❌ 错误'}")
        logger.info(f"验证错误密码 (哈希1): {'✅ 正确' if result3 else '❌ 错误'}")
        
    except Exception as e:
        logger.error(f"测试密码函数时发生错误: {e}", exc_info=True)

def create_test_user():
    """创建一个测试用户来验证登录功能"""
    try:
        logger.info("\n=== 创建测试用户 ===")
        
        # 创建数据库连接
        db = SessionLocal()
        
        try:
            # 检查是否已存在测试用户
            existing_user = db.query(User).filter(User.username == "testlogin").first()
            if existing_user:
                logger.info("测试用户已存在，删除后重新创建")
                db.delete(existing_user)
                db.commit()
            
            # 创建新的测试用户
            from datetime import datetime
            import uuid
            
            # 使用正确的密码哈希生成方式
            password_hash = get_password_hash("password123")
            
            test_user = User(
                user_id=uuid.uuid4(),
                username="testlogin",
                email="testlogin@example.com",
                phone="13800138000",
                display_name="测试用户",
                password_hash=password_hash,
                is_active='Y',
                is_superuser=False,
                created_at=datetime.utcnow()
            )
            
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            
            logger.info("✅ 测试用户创建成功")
            logger.info(f"用户名: {test_user.username}")
            logger.info(f"密码: password123")
            logger.info(f"邮箱: {test_user.email}")
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"创建测试用户时发生错误: {e}", exc_info=True)

def create_actual_user():
    """为用户创建实际的登录账号"""
    try:
        logger.info("\n=== 创建实际用户账号 ===")
        
        # 创建数据库连接
        db = SessionLocal()
        
        try:
            # 用户尝试登录的邮箱
            user_email = "xxiaochang@qq.com"
            user_password = "password123"  # 使用相同的密码便于测试
            
            # 检查用户是否已存在
            existing_user = db.query(User).filter(
                (User.email == user_email) | 
                (User.username == "xxiaochang")
            ).first()
            
            if existing_user:
                logger.info("用户账号已存在，更新密码")
                # 更新密码哈希
                existing_user.password_hash = get_password_hash(user_password)
                db.commit()
                logger.info(f"✅ 用户密码已更新")
                logger.info(f"邮箱: {existing_user.email}")
                logger.info(f"用户名: {existing_user.username}")
                logger.info(f"密码: {user_password}")
            else:
                # 创建新用户
                from datetime import datetime
                import uuid
                
                # 使用正确的密码哈希生成方式
                password_hash = get_password_hash(user_password)
                
                actual_user = User(
                    user_id=uuid.uuid4(),
                    username="xxiaochang",
                    email=user_email,
                    phone="13160697108",
                    display_name="小常",
                    password_hash=password_hash,
                    is_active='Y',
                    is_superuser=False,
                    created_at=datetime.utcnow()
                )
                
                db.add(actual_user)
                db.commit()
                db.refresh(actual_user)
                
                logger.info("✅ 实际用户账号创建成功")
                logger.info(f"用户名: {actual_user.username}")
                logger.info(f"密码: {user_password}")
                logger.info(f"邮箱: {actual_user.email}")
                logger.info(f"手机号: {actual_user.phone}")
                
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"创建实际用户账号时发生错误: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    logger.info("开始检查用户密码信息...")
    
    # 测试密码函数
    test_password_functions()
    
    # 检查现有用户密码
    check_user_passwords()
    
    # 创建测试用户
    create_test_user()
    
    logger.info("\n检查完成")

if __name__ == "__main__":
    main()
    # 创建实际用户
    create_actual_user()
