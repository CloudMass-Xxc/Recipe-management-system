"""
AI服务模块异常类定义
"""
from fastapi import HTTPException


class AIServiceError(HTTPException):
    """
    AI服务基础异常类
    """
    def __init__(self, detail: str = "AI service error", status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)


class APIConnectionError(AIServiceError):
    """
    API连接错误
    """
    def __init__(self, detail: str = "Failed to connect to AI API"):
        super().__init__(detail=detail, status_code=503)


class InvalidResponseError(AIServiceError):
    """
    无效响应错误
    """
    def __init__(self, detail: str = "Invalid response from AI API"):
        super().__init__(detail=detail, status_code=500)


class RateLimitError(AIServiceError):
    """
    速率限制错误
    """
    def __init__(self, detail: str = "API rate limit exceeded"):
        super().__init__(detail=detail, status_code=429)


class AuthenticationError(AIServiceError):
    """
    认证错误
    """
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail=detail, status_code=401)


class InvalidRecipeParametersError(AIServiceError):
    """
    无效的食谱参数错误
    """
    def __init__(self, detail: str = "Invalid recipe parameters"):
        super().__init__(detail=detail, status_code=400)


class RecipeGenerationError(AIServiceError):
    """
    食谱生成错误
    """
    def __init__(self, detail: str = "Failed to generate recipe"):
        super().__init__(detail=detail, status_code=500)


class RecipeEnhancementError(AIServiceError):
    """
    食谱增强错误
    """
    def __init__(self, detail: str = "Failed to enhance recipe"):
        super().__init__(detail=detail, status_code=500)