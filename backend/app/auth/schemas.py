from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# 用户创建请求
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., min_length=6, description="密码")
    display_name: str = Field(..., min_length=1, max_length=255, description="显示名称")
    diet_preferences: Optional[List[str]] = Field(None, description="饮食偏好")

# 用户登录请求
class UserLogin(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

# 令牌响应
class Token(BaseModel):
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")

# 令牌数据
class TokenData(BaseModel):
    user_id: Optional[str] = Field(None, description="用户ID")
    username: Optional[str] = Field(None, description="用户名")

# 用户信息
class UserInfo(BaseModel):
    user_id: str = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    display_name: str = Field(..., description="显示名称")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    bio: Optional[str] = Field(None, description="个人简介")
    diet_preferences: Optional[List[str]] = Field(None, description="饮食偏好")
    created_at: datetime = Field(..., description="创建时间")
    
    class Config:
        from_attributes = True

# 用户更新请求
class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, min_length=1, max_length=255, description="显示名称")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    bio: Optional[str] = Field(None, description="个人简介")
    diet_preferences: Optional[List[str]] = Field(None, description="饮食偏好")

# 密码更新请求
class PasswordUpdate(BaseModel):
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")

# 响应消息
class Message(BaseModel):
    message: str = Field(..., description="消息")
    success: bool = Field(..., description="是否成功")
    data: Optional[Dict[str, Any]] = Field(None, description="附加数据")