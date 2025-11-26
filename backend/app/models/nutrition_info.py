from sqlalchemy import Column, String, Float, ForeignKey, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class NutritionInfo(Base):
    __tablename__ = "nutrition_info"
    
    nutrition_id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="营养信息ID")
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.recipe_id", ondelete="CASCADE"), unique=True, nullable=False, comment="食谱ID")
    calories = Column(Float, nullable=False, comment="卡路里")
    protein = Column(Float, nullable=False, comment="蛋白质(g)")
    carbs = Column(Float, nullable=False, comment="碳水化合物(g)")
    fat = Column(Float, nullable=False, comment="脂肪(g)")
    fiber = Column(Float, nullable=True, comment="纤维(g)")
    sugar = Column(Float, nullable=True, comment="糖(g)")
    sodium = Column(Float, nullable=True, comment="钠(mg)")
    additional_nutrients = Column(JSON, nullable=True, comment="其他营养信息")
    
    # 关系
    recipe = relationship("Recipe", back_populates="nutrition_info")