from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class DietPlan(Base):
    __tablename__ = "diet_plans"
    
    plan_id = Column(String(36), primary_key=True, index=True, comment="饮食计划ID")
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    name = Column(String(255), nullable=False, comment="计划名称")
    description = Column(Text, nullable=True, comment="计划描述")
    start_date = Column(DateTime(timezone=True), nullable=False, comment="开始日期")
    end_date = Column(DateTime(timezone=True), nullable=True, comment="结束日期")
    meal_plan = Column(JSON, nullable=False, comment="每日餐食计划(JSON)")
    goal = Column(String(255), nullable=True, comment="目标")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    user = relationship("User", back_populates="diet_plans")