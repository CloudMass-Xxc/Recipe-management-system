from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Rating(Base):
    __tablename__ = "ratings"
    
    rating_id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="评分ID")
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    recipe_id = Column(String(36), ForeignKey("recipes.recipe_id", ondelete="CASCADE"), nullable=False, comment="食谱ID")
    score = Column(Integer, nullable=False, comment="评分(1-5)")
    comment = Column(Text, nullable=True, comment="评论")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="评分时间")
    
    # 关系
    user = relationship("User", back_populates="ratings")
    recipe = relationship("Recipe", back_populates="ratings")
    
    # 唯一约束，确保用户不会重复评分同一食谱
    __table_args__ = (
        UniqueConstraint('user_id', 'recipe_id', name='_user_recipe_rating_uc'),
    )