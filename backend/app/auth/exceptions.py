from fastapi import HTTPException, status
from typing import Optional

# 自定义认证异常类
class AuthException(HTTPException):
    """
    认证相关的异常基类
    """
    def __init__(self, detail: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(status_code=status_code, detail=detail)

# 凭证错误异常
class CredentialsException(AuthException):
    """
    凭证错误异常
    """
    def __init__(self, detail: str = "无法验证凭证"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

# 令牌过期异常
class TokenExpiredException(AuthException):
    """
    令牌过期异常
    """
    def __init__(self, detail: str = "令牌已过期"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

# 用户不存在异常
class UserNotFoundException(AuthException):
    """
    用户不存在异常
    """
    def __init__(self, detail: str = "用户不存在"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)

# 用户已存在异常
class UserAlreadyExistsException(AuthException):
    """
    用户已存在异常
    """
    def __init__(self, detail: str = "用户已存在"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)

# 密码错误异常
class IncorrectPasswordException(AuthException):
    """
    密码错误异常
    """
    def __init__(self, detail: str = "密码错误"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

# 权限不足异常
class PermissionDeniedException(AuthException):
    """
    权限不足异常
    """
    def __init__(self, detail: str = "权限不足"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)