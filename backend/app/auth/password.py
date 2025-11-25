from passlib.context import CryptContext
from typing import Optional

# 创建密码上下文
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], 
                          default="pbkdf2_sha256",
                          pbkdf2_sha256__default_rounds=100000,  # 保持安全的迭代轮数
                          deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    获取密码的哈希值
    
    Args:
        password: 原始密码
    
    Returns:
        密码的哈希值
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码
    
    Returns:
        密码是否匹配
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False