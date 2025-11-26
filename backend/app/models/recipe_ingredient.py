from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="关联ID")
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.recipe_id", ondelete="CASCADE"), nullable=False, comment="食谱ID")
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingredient_id", ondelete="CASCADE"), nullable=False, comment="食材ID")
    quantity = Column(Float, nullable=False, comment="数量")
    unit = Column(String(50), nullable=True, comment="单位")
    
    # 关系
    recipe = relationship("Recipe")
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")