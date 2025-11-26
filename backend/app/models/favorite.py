from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Favorite(Base):
    __tablename__ = "favorites"
    
    favorite_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=func.uuid_generate_v4(), comment="收藏ID")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.recipe_id", ondelete="CASCADE"), nullable=False, comment="食谱ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="收藏时间")
    
    # 关系
    user = relationship("User", back_populates="favorites")
    recipe = relationship("Recipe", back_populates="favorites")
    
    # 唯一约束，确保用户不会重复收藏同一食谱
    __table_args__ = (
        UniqueConstraint('user_id', 'recipe_id', name='_user_recipe_uc'),
    )