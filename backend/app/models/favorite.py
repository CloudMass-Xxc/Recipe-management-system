from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
import logging

# 配置日志记录器
logger = logging.getLogger(__name__)

class Favorite(Base):
    __tablename__ = "favorites"
    
    favorite_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, comment="收藏ID")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.recipe_id", ondelete="CASCADE"), nullable=False, comment="食谱ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="收藏时间")
    
    # 关系
    user = relationship("User", back_populates="favorites")
    recipe = relationship("Recipe", back_populates="favorites")
    
    def __repr__(self):
        return f"<Favorite(favorite_id={self.favorite_id}, user_id={self.user_id}, recipe_id={self.recipe_id})>"
    
    @classmethod
    def get_by_user_and_recipe(cls, db, user_id, recipe_id):
        """
        通过用户ID和食谱ID获取收藏记录
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            recipe_id: 食谱ID
            
        Returns:
            Favorite: 收藏记录对象
        """
        logger.info(f"[DATA_SOURCE_VERIFICATION] Querying Favorite by user_id: {user_id} and recipe_id: {recipe_id} from DATABASE")
        favorite = db.query(cls).filter(
            cls.user_id == user_id,
            cls.recipe_id == recipe_id
        ).first()
        return favorite
    
    @classmethod
    def get_by_user(cls, db, user_id, page=1, limit=10):
        """
        获取用户的所有收藏记录，支持分页
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            page: 页码
            limit: 每页数量
            
        Returns:
            List[Favorite]: 收藏记录列表
            int: 总记录数
        """
        logger.info(f"[DATA_SOURCE_VERIFICATION] Querying Favorites by user_id: {user_id} with page: {page}, limit: {limit} from DATABASE")
        query = db.query(cls).filter(cls.user_id == user_id).order_by(cls.created_at.desc())
        total = query.count()
        favorites = query.offset((page - 1) * limit).limit(limit).all()
        return favorites, total
    
    def save(self, db):
        """
        保存收藏记录
        
        Args:
            db: 数据库会话
        """
        logger.info(f"[DATA_SOURCE_VERIFICATION] Creating Favorite: {self} in DATABASE")
        db.add(self)
        db.commit()
        db.refresh(self)
        logger.info(f"[DATA_SOURCE_VERIFICATION] Favorite {self} created successfully in DATABASE")
        return self
    
    def delete(self, db):
        """
        删除收藏记录
        
        Args:
            db: 数据库会话
        """
        logger.info(f"[DATA_SOURCE_VERIFICATION] Deleting Favorite: {self} from DATABASE")
        db.delete(self)
        db.commit()
        logger.info(f"[DATA_SOURCE_VERIFICATION] Favorite {self} deleted successfully from DATABASE")
