from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Ingredient(Base):
    __tablename__ = "ingredients"
    
    ingredient_id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="食材ID")
    name = Column(String(255), nullable=False, comment="食材名称")
    category = Column(String(100), nullable=True, index=True, comment="食材类别")
    unit = Column(String(50), nullable=True, comment="单位")
    nutrition_data = Column(JSON, nullable=True, comment="营养数据")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    # 关系
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient", cascade="all, delete-orphan")