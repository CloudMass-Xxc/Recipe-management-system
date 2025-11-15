from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from app.core.config import settings

# 生成访问令牌
def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量
    
    Returns:
        JWT令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# 验证令牌
def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    验证令牌
    
    Args:
        token: JWT令牌
    
    Returns:
        解码后的数据，如果令牌无效则返回None
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

# 获取令牌中的用户ID
def get_user_id_from_token(token: str) -> Optional[str]:
    """
    从令牌中获取用户ID
    
    Args:
        token: JWT令牌
    
    Returns:
        用户ID，如果令牌无效则返回None
    """
    payload = verify_token(token)
    if payload and "sub" in payload:
        return payload["sub"]
    return None