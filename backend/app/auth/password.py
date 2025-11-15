from passlib.context import CryptContext
from typing import Optional

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    return pwd_context.verify(plain_password, hashed_password)

def generate_user_id() -> str:
    """
    生成用户ID（UUID）
    
    Returns:
        用户ID
    """
    import uuid
    return str(uuid.uuid4())

def generate_recipe_id() -> str:
    """
    生成食谱ID（UUID）
    
    Returns:
        食谱ID
    """
    import uuid
    return str(uuid.uuid4())

def generate_plan_id() -> str:
    """
    生成饮食计划ID（UUID）
    
    Returns:
        饮食计划ID
    """
    import uuid
    return str(uuid.uuid4())