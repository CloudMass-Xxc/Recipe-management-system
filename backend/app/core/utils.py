import uuid
import secrets
import string

def generate_recipe_id() -> str:
    """
    生成食谱ID
    
    Returns:
        生成的食谱ID字符串
    """
    return str(uuid.uuid4())

def generate_random_string(length: int = 16) -> str:
    """
    生成随机字符串
    
    Args:
        length: 字符串长度
    
    Returns:
        随机生成的字符串
    """
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_unique_id(prefix: str = "") -> str:
    """
    生成带前缀的唯一ID
    
    Args:
        prefix: ID前缀
    
    Returns:
        带前缀的唯一ID
    """
    unique_part = str(uuid.uuid4()).replace("-", "")
    if prefix:
        return f"{prefix}_{unique_part}"
    return unique_part
