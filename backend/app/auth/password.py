from passlib.context import CryptContext
import logging
import traceback

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 创建密码上下文，用于密码哈希和验证
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    获取密码的哈希值
    
    Args:
        password: 原始密码
    
    Returns:
        str: 密码的哈希值
    """
    try:
        # 使用pbkdf2_sha256算法，不再需要密码截断（但保留作为安全措施）
        truncated_password = password[:72]
        if len(password) > 72:
            logger.warning(f"密码长度超过72字符，已截断: 原始长度={len(password)}, 截断后长度={len(truncated_password)}")
        
        hashed_password = pwd_context.hash(truncated_password)
        logger.info("密码哈希生成成功")
        return hashed_password
    except Exception as e:
        logger.error(f"密码哈希生成失败: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise Exception(f"密码哈希生成失败: {str(e)}")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码
    
    Returns:
        bool: 密码是否匹配
    """
    try:
        # 截断密码到72个字符，保持一致性
        truncated_password = plain_password[:72]
        if len(plain_password) > 72:
            logger.warning(f"验证密码长度超过72字符，已截断: 原始长度={len(plain_password)}, 截断后长度={len(truncated_password)}")
        
        is_verified = pwd_context.verify(truncated_password, hashed_password)
        logger.info(f"密码验证结果: {'成功' if is_verified else '失败'}")
        return is_verified
    except Exception as e:
        logger.error(f"密码验证失败: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        return False  # 验证过程出错时，安全起见返回False
