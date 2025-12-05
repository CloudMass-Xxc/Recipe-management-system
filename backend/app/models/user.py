from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import logging

# 配置日志记录器
logger = logging.getLogger(__name__)

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, comment="用户ID")
    username = Column(String(100), unique=True, index=True, nullable=False, comment="用户名")
    email = Column(String(255), unique=True, index=True, nullable=False, comment="邮箱")
    phone = Column(String(20), unique=True, nullable=True, index=True, comment="手机号")
    password_hash = Column(String(255), nullable=False, comment="哈希后的密码")
    # 兼容现有数据库结构，将以下字段设为可为空或提供默认值
    display_name = Column(String(255), nullable=True, default=None, comment="显示名称")
    avatar_url = Column(String(500), nullable=True, default=None, comment="头像URL")
    bio = Column(Text, nullable=True, default=None, comment="个人简介")
    diet_preferences = Column(JSON, nullable=True, default=None, comment="饮食偏好")
    is_active = Column(String(1), default='Y', comment="是否激活")  # VARCHAR(1)类型，使用'Y'/'N'
    is_superuser = Column(Boolean, default=False, comment="是否为超级用户")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 登录安全相关字段
    failed_login_attempts = Column(Integer, default=0, comment="登录失败次数")
    locked_until = Column(DateTime(timezone=True), nullable=True, comment="账户锁定截止时间")
    
    # 关系
    recipes = relationship("Recipe", back_populates="author", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    diet_plans = relationship("DietPlan", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}', email='{self.email}')>"
    
    @classmethod
    def get_by_id(cls, db, user_id):
        """
        通过ID获取用户，记录数据来源
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            User: 用户对象
        """
        logger.info(f"[DATA_SOURCE_VERIFICATION] Querying User by ID: {user_id} from DATABASE")
        user = db.query(cls).filter(cls.user_id == user_id).first()
        if user:
            logger.info(f"[DATA_SOURCE_VERIFICATION] Retrieved User: {user} from DATABASE")
        else:
            logger.info(f"[DATA_SOURCE_VERIFICATION] User with ID {user_id} not found in DATABASE")
        return user
    
    @classmethod
    def get_by_username(cls, db, username):
        """
        通过用户名获取用户，记录数据来源
        
        Args:
            db: 数据库会话
            username: 用户名
            
        Returns:
            User: 用户对象
        """
        logger.info(f"[DATA_SOURCE_VERIFICATION] Querying User by username: '{username}' from DATABASE")
        user = db.query(cls).filter(cls.username == username).first()
        if user:
            logger.info(f"[DATA_SOURCE_VERIFICATION] Retrieved User: {user} from DATABASE")
        else:
            logger.info(f"[DATA_SOURCE_VERIFICATION] User with username '{username}' not found in DATABASE")
        return user
    
    @classmethod
    def get_by_email(cls, db, email):
        """
        通过邮箱获取用户，记录数据来源
        
        Args:
            db: 数据库会话
            email: 邮箱
            
        Returns:
            User: 用户对象
        """
        logger.info(f"[DATA_SOURCE_VERIFICATION] Querying User by email: '{email}' from DATABASE")
        user = db.query(cls).filter(cls.email == email).first()
        if user:
            logger.info(f"[DATA_SOURCE_VERIFICATION] Retrieved User: {user} from DATABASE")
        else:
            logger.info(f"[DATA_SOURCE_VERIFICATION] User with email '{email}' not found in DATABASE")
        return user
    
    @classmethod
    def get_by_phone(cls, db, phone):
        """
        通过手机号获取用户，记录数据来源
        
        Args:
            db: 数据库会话
            phone: 手机号
            
        Returns:
            User: 用户对象
        """
        logger.info(f"[DATA_SOURCE_VERIFICATION] Querying User by phone: '{phone}' from DATABASE")
        user = db.query(cls).filter(cls.phone == phone).first()
        if user:
            logger.info(f"[DATA_SOURCE_VERIFICATION] Retrieved User: {user} from DATABASE")
        else:
            logger.info(f"[DATA_SOURCE_VERIFICATION] User with phone '{phone}' not found in DATABASE")
        return user
    
    def save(self, db):
        """
        保存用户数据，记录数据操作
        
        Args:
            db: 数据库会话
        """
        if self.user_id:
            logger.info(f"[DATA_SOURCE_VERIFICATION] Updating User: {self} in DATABASE")
        else:
            logger.info(f"[DATA_SOURCE_VERIFICATION] Creating User: {self} in DATABASE")
        
        db.add(self)
        db.commit()
        db.refresh(self)
        
        logger.info(f"[DATA_SOURCE_VERIFICATION] User {self} {'updated' if hasattr(self, 'user_id') else 'created'} successfully in DATABASE")
        return self
    
    def delete(self, db):
        """
        删除用户数据，记录数据操作
        
        Args:
            db: 数据库会话
        """
        logger.info(f"[DATA_SOURCE_VERIFICATION] Deleting User: {self} from DATABASE")
        db.delete(self)
        db.commit()
        logger.info(f"[DATA_SOURCE_VERIFICATION] User {self} deleted successfully from DATABASE")
    
    @property
    def is_active_boolean(self):
        """
        将字符串类型的is_active转换为布尔值，用于Pydantic模型验证
        
        Returns:
            bool: True如果is_active为'Y'，否则为False
        """
        return self.is_active == 'Y'
    