from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User
from app.auth.password import get_password_hash
from app.auth.exceptions import UserNotFoundException, UserAlreadyExistsException

class UserService:
    """
    用户服务类，处理用户相关的业务逻辑
    """
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """
        根据ID获取用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
        
        Returns:
            用户对象，如果不存在则返回None
        """
        return db.query(User).filter(User.user_id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        
        Args:
            db: 数据库会话
            username: 用户名
        
        Returns:
            用户对象，如果不存在则返回None
        """
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        
        Args:
            db: 数据库会话
            email: 邮箱
        
        Returns:
            用户对象，如果不存在则返回None
        """
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None) -> List[User]:
        """
        获取用户列表
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的记录数
            is_active: 是否筛选活跃用户
        
        Returns:
            用户列表
        """
        query = db.query(User)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_user(db: Session, user_id: str, **kwargs) -> User:
        """
        更新用户信息
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            **kwargs: 要更新的字段
        
        Returns:
            更新后的用户对象
        
        Raises:
            UserNotFoundException: 如果用户不存在
        """
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise UserNotFoundException()
        
        # 如果包含密码字段，需要哈希处理
        if "password" in kwargs:
            kwargs["password_hash"] = get_password_hash(kwargs.pop("password"))
        
        # 更新用户信息
        for field, value in kwargs.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def deactivate_user(db: Session, user_id: str) -> User:
        """
        停用用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
        
        Returns:
            更新后的用户对象
        
        Raises:
            UserNotFoundException: 如果用户不存在
        """
        return UserService.update_user(db, user_id, is_active=False)
    
    @staticmethod
    def activate_user(db: Session, user_id: str) -> User:
        """
        激活用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
        
        Returns:
            更新后的用户对象
        
        Raises:
            UserNotFoundException: 如果用户不存在
        """
        return UserService.update_user(db, user_id, is_active=True)
    
    @staticmethod
    def count_users(db: Session, is_active: Optional[bool] = None) -> int:
        """
        统计用户数量
        
        Args:
            db: 数据库会话
            is_active: 是否统计活跃用户
        
        Returns:
            用户数量
        """
        query = db.query(User)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.count()
    
    @staticmethod
    def search_users(db: Session, query_text: str, skip: int = 0, limit: int = 100) -> List[User]:
        """
        搜索用户
        
        Args:
            db: 数据库会话
            query_text: 搜索文本（用户名或显示名称）
            skip: 跳过的记录数
            limit: 返回的记录数
        
        Returns:
            用户列表
        """
        return db.query(User).filter(
            (User.username.ilike(f"%{query_text}%") | 
             User.display_name.ilike(f"%{query_text}%"))
        ).offset(skip).limit(limit).all()