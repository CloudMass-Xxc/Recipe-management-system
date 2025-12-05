from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="电子邮箱")
    phone: Optional[str] = Field(None, description="手机号码")


class UserCreate(UserBase):
    """用户注册模型"""
    password: str = Field(..., min_length=6, description="密码，至少6位字符")
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """验证密码非空且至少6位字符"""
        if not v or len(v) < 6:
            raise ValueError('密码不能为空且至少需要6位字符')
        return v
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """验证手机号码格式（可选）"""
        if v and not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('手机号码格式不正确')
        return v


class UserLogin(BaseModel):
    """用户登录模型"""
    username: str = Field(..., description="用户名、邮箱或手机号")
    password: str = Field(..., description="密码")


class UserResponse(UserBase):
    """用户响应模型"""
    user_id: str
    is_active: bool
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """令牌响应模型"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class LoginResponse(BaseModel):
    """登录响应模型"""
    message: str
    success: bool
    data: Optional[TokenResponse] = None


class RegisterResponse(BaseModel):
    """注册响应模型"""
    message: str
    success: bool
    data: Optional[UserResponse] = None
