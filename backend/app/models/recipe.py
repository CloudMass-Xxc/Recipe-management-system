from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    
    recipe_id = Column(String(36), primary_key=True, index=True, comment="食谱ID")
    title = Column(String(255), nullable=False, index=True, comment="标题")
    description = Column(Text, nullable=True, comment="描述")
    instructions = Column(Text, nullable=False, comment="烹饪步骤")
    cooking_time = Column(Integer, nullable=False, comment="烹饪时间(分钟)")
    servings = Column(Integer, nullable=False, comment="份量")
    difficulty = Column(String(50), nullable=False, index=True, comment="难度")
    author_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="作者ID")
    ingredients = Column(JSON, nullable=True, comment="食材列表(JSON)")
    tags = Column(JSON, nullable=True, index=True, comment="标签列表(JSON)")
    image_url = Column(String(500), nullable=True, comment="图片URL")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    author = relationship("User", back_populates="recipes")
    nutrition_info = relationship("NutritionInfo", back_populates="recipe", uselist=False, cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="recipe", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="recipe", cascade="all, delete-orphan")