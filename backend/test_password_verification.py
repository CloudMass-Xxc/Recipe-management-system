#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试密码验证逻辑并重置用户密码
"""

import sys
import logging
from app.auth.password import verify_password, get_password_hash
from app.models.user import User
from app.core.database import get_db
from sqlalchemy.orm import Session

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('password_test_script')

def test_password_verification():
    """测试密码验证逻辑"""
    logger.info("=== 测试密码验证逻辑 ===")
    
    # 测试密码
    test_password = "password123"
    
    # 生成密码哈希
    hashed_password = get_password_hash(test_password)
    logger.info(f"原始密码: {test_password}")
    logger.info(f"密码哈希: {hashed_password}")
    
    # 验证正确密码
    result_correct = verify_password(test_password, hashed_password)
    logger.info(f"验证正确密码: {'成功' if result_correct else '失败'}")
    
    # 验证错误密码
    result_incorrect = verify_password("wrongpassword", hashed_password)
    logger.info(f"验证错误密码: {'失败(正确)' if not result_incorrect else '成功(错误)'}")
    
    return {
        "correct_password_test": result_correct,
        "incorrect_password_test": not result_incorrect
    }

def check_user_password(db: Session, username: str, test_password: str):
    """检查用户密码"""
    logger.info(f"\n=== 检查用户 {username} 的密码 ===")
    
    # 获取用户
    user = User.get_by_username(db, username)
    if not user:
        logger.error(f"用户 {username} 不存在")
        return False
    
    logger.info(f"找到用户: {user.username}")
    logger.info(f"用户密码哈希: {user.password_hash}")
    
    # 尝试验证密码
    is_valid = verify_password(test_password, user.password_hash)
    logger.info(f"密码 '{test_password}' 验证结果: {'成功' if is_valid else '失败'}")
    
    return is_valid

def reset_user_password(db: Session, username: str, new_password: str):
    """重置用户密码"""
    logger.info(f"\n=== 重置用户 {username} 的密码 ===")
    
    # 获取用户
    user = User.get_by_username(db, username)
    if not user:
        logger.error(f"用户 {username} 不存在")
        return False
    
    # 生成新密码哈希
    new_hashed_password = get_password_hash(new_password)
    
    # 更新密码
    user.password_hash = new_hashed_password
    db.commit()
    db.refresh(user)
    
    logger.info(f"密码已重置为: {new_password}")
    logger.info(f"新密码哈希: {user.password_hash}")
    
    # 验证新密码
    is_valid = verify_password(new_password, user.password_hash)
    logger.info(f"新密码验证结果: {'成功' if is_valid else '失败'}")
    
    return is_valid

def main():
    """主函数"""
    logger.info("开始测试密码验证和重置...")
    
    # 测试密码验证逻辑
    password_test_results = test_password_verification()
    
    # 如果密码验证逻辑正常，继续检查和重置用户密码
    if password_test_results["correct_password_test"] and password_test_results["incorrect_password_test"]:
        logger.info("\n✅ 密码验证逻辑正常工作")
        
        # 获取数据库会话
        db = next(get_db())
        
        # 检查用户密码
        user_to_check = "xxiaochang"
        test_password = "password123"
        
        is_password_valid = check_user_password(db, user_to_check, test_password)
        
        if not is_password_valid:
            logger.info("\n密码验证失败，尝试重置密码...")
            
            # 重置用户密码
            reset_success = reset_user_password(db, user_to_check, test_password)
            
            if reset_success:
                logger.info("\n✅ 密码重置成功！")
                logger.info("现在可以使用新密码登录了")
            else:
                logger.error("\n❌ 密码重置失败")
        else:
            logger.info("\n✅ 用户密码验证成功")
    else:
        logger.error("\n❌ 密码验证逻辑存在问题")
    
    logger.info("\n测试完成")

if __name__ == "__main__":
    main()
