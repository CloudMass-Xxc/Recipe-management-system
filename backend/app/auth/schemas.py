from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# User schemas

class UserBase(BaseModel):
    """基础用户模型"""
    username: str = Field(..., min_length=3, max_length=100, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    phone: Optional[str] = Field(None, description="手机号")

class UserCreate(UserBase):
    """用户创建请求"""
    password: str = Field(..., min_length=6, description="密码")
    display_name: Optional[str] = Field(None, max_length=255, description="显示名称")

class UserLogin(BaseModel):
    """用户登录请求"""
    identifier: str = Field(..., min_length=3, description="登录标识（手机号/邮箱/用户名）")
    password: str = Field(..., min_length=6, description="密码")

class Token(BaseModel):
    """令牌响应"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")

class TokenData(BaseModel):
    """令牌数据"""
    user_id: Optional[str] = Field(None, description="用户ID")

class UserResponse(UserBase):
    """用户响应模型"""
    user_id: str = Field(..., description="用户ID")
    display_name: Optional[str] = Field(None, description="显示名称")
    created_at: datetime = Field(..., description="创建时间")
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """用户更新请求"""
    display_name: Optional[str] = Field(None, min_length=1, max_length=255, description="显示名称")
    phone: Optional[str] = Field(None, description="手机号")

class PasswordUpdate(BaseModel):
    """密码更新请求"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")

class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    user: UserResponse