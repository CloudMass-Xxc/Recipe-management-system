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
        JWT访问令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "sub": str(data.get("sub"))  # 确保用户ID是字符串类型
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# 生成刷新令牌
def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    创建刷新令牌
    
    Args:
        data: 要编码的数据
    
    Returns:
        JWT刷新令牌
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "sub": str(data.get("sub"))  # 确保用户ID是字符串类型
    })
    
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
    except Exception:
        return None

# 刷新访问令牌
def refresh_access_token(refresh_token: str) -> Optional[str]:
    """
    使用刷新令牌生成新的访问令牌
    
    Args:
        refresh_token: JWT刷新令牌
    
    Returns:
        新的访问令牌，如果刷新令牌无效则返回None
    """
    payload = verify_token(refresh_token)
    if not payload or "sub" not in payload:
        return None
    
    user_id = payload["sub"]
    return create_access_token(data={"sub": user_id})