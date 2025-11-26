from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, comment="用户ID")
    username = Column(String(100), unique=True, index=True, nullable=False, comment="用户名")
    email = Column(String(255), unique=True, index=True, nullable=False, comment="邮箱")
    phone = Column(String(20), unique=True, nullable=True, index=True, comment="手机号")
    password_hash = Column(String(255), nullable=False, comment="哈希后的密码")
    display_name = Column(String(255), nullable=False, comment="显示名称")
    avatar_url = Column(String(500), nullable=True, comment="头像URL")
    bio = Column(Text, nullable=True, comment="个人简介")
    diet_preferences = Column(JSON, nullable=True, comment="饮食偏好")
    is_active = Column(String(1), default='Y', comment="是否激活")  # VARCHAR(1)类型，使用'Y'/'N'
    is_superuser = Column(Boolean, default=False, comment="是否为超级用户")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 登录安全相关字段
    failed_login_attempts = Column(Integer, default=0, comment="登录失败次数")
    locked_until = Column(DateTime(timezone=True), nullable=True, comment="账户锁定截止时间")
    
    # 关系
    recipes = relationship("Recipe", back_populates="author", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    diet_plans = relationship("DietPlan", back_populates="user", cascade="all, delete-orphan")