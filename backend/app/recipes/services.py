from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
from typing import List, Optional, Dict, Any
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.recipe_ingredient import RecipeIngredient
from app.models.nutrition_info import NutritionInfo
from app.models.favorite import Favorite
from app.models.rating import Rating
from app.models.user import User
from app.core.utils import generate_recipe_id

class RecipeService:
    """
    食谱服务类，处理食谱相关的业务逻辑
    """
    
    @staticmethod
    def create_recipe(db: Session, author_id: str, recipe_data: Dict[str, Any]) -> Recipe:
        """
        创建新食谱
        
        Args:
            db: 数据库会话
            author_id: 作者ID
            recipe_data: 食谱数据
        
        Returns:
            创建的食谱对象
        """
        # 提取营养信息
        nutrition_info = recipe_data.pop("nutrition_info", None)
        ingredients = recipe_data.pop("ingredients", [])
        
        # 创建食谱
        new_recipe = Recipe(
            recipe_id=generate_recipe_id(),
            author_id=author_id,
            **recipe_data
        )
        db.add(new_recipe)
        db.flush()  # 获取recipe_id但不提交事务
        
        # 创建营养信息
        if nutrition_info:
            new_nutrition = NutritionInfo(
                recipe_id=new_recipe.recipe_id,
                **nutrition_info
            )
            db.add(new_nutrition)
        
        # 处理食材
        for ingredient_data in ingredients:
            # 查找或创建食材
            ingredient = db.query(Ingredient).filter(
                Ingredient.name == ingredient_data["name"]
            ).first()
            
            if not ingredient:
                ingredient = Ingredient(
                    name=ingredient_data["name"],
                    unit=ingredient_data.get("unit")
                )
                db.add(ingredient)
                db.flush()  # 获取ingredient_id
            
            # 创建食谱-食材关联
            recipe_ingredient = RecipeIngredient(
                recipe_id=new_recipe.recipe_id,
                ingredient_id=ingredient.ingredient_id,
                quantity=ingredient_data["quantity"],
                unit=ingredient_data.get("unit"),
                note=ingredient_data.get("note")
            )
            db.add(recipe_ingredient)
        
        db.commit()
        db.refresh(new_recipe)
        return new_recipe
    
    @staticmethod
    def get_recipe_by_id(db: Session, recipe_id: str, load_relationships: bool = True) -> Optional[Recipe]:
        """
        根据ID获取食谱
        
        Args:
            db: 数据库会话
            recipe_id: 食谱ID
            load_relationships: 是否加载关联数据
        
        Returns:
            食谱对象，如果不存在则返回None
        """
        query = db.query(Recipe)
        
        if load_relationships:
            query = query.options(
                joinedload(Recipe.author),
                joinedload(Recipe.nutrition_info)
            )
        
        return query.filter(Recipe.recipe_id == recipe_id).first()
    
    @staticmethod
    def get_recipes(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        author_id: Optional[str] = None,
        search_params: Optional[Dict[str, Any]] = None
    ) -> List[Recipe]:
        """
        获取食谱列表
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的记录数
            author_id: 作者ID（可选）
            search_params: 搜索参数（可选）
        
        Returns:
            食谱列表
        """
        query = db.query(Recipe).options(
            joinedload(Recipe.author)
        )
        
        # 按作者筛选
        if author_id:
            query = query.filter(Recipe.author_id == author_id)
        
        # 应用搜索条件
        if search_params:
            # 关键词搜索
            if search_params.get("query"):
                search_text = f"%{search_params['query']}%"
                query = query.filter(
                    or_(
                        Recipe.title.ilike(search_text),
                        Recipe.description.ilike(search_text)
                    )
                )
            
            # 按标签筛选
            if search_params.get("tags"):
                for tag in search_params["tags"]:
                    query = query.filter(Recipe.tags.contains([tag]))
            
            # 按难度筛选
            if search_params.get("difficulty"):
                query = query.filter(Recipe.difficulty == search_params["difficulty"])
            
            # 按烹饪时间筛选
            if search_params.get("max_cooking_time"):
                query = query.filter(Recipe.cooking_time <= search_params["max_cooking_time"])
        
        # 按创建时间降序排序
        query = query.order_by(Recipe.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_recipe(db: Session, recipe_id: str, recipe_data: Dict[str, Any]) -> Optional[Recipe]:
        """
        更新食谱
        
        Args:
            db: 数据库会话
            recipe_id: 食谱ID
            recipe_data: 更新数据
        
        Returns:
            更新后的食谱对象，如果不存在则返回None
        """
        recipe = RecipeService.get_recipe_by_id(db, recipe_id)
        if not recipe:
            return None
        
        # 提取需要特殊处理的字段
        nutrition_info = recipe_data.pop("nutrition_info", None)
        ingredients = recipe_data.pop("ingredients", None)
        
        # 更新基本信息
        for field, value in recipe_data.items():
            if hasattr(recipe, field):
                setattr(recipe, field, value)
        
        # 更新营养信息
        if nutrition_info is not None:
            if recipe.nutrition_info:
                # 更新现有营养信息
                for field, value in nutrition_info.items():
                    setattr(recipe.nutrition_info, field, value)
            elif nutrition_info:
                # 创建新的营养信息
                new_nutrition = NutritionInfo(
                    recipe_id=recipe.recipe_id,
                    **nutrition_info
                )
                db.add(new_nutrition)
        
        # 更新食材
        if ingredients is not None:
            # 删除现有食材关联
            db.query(RecipeIngredient).filter(
                RecipeIngredient.recipe_id == recipe_id
            ).delete()
            
            # 添加新食材关联
            for ingredient_data in ingredients:
                ingredient = db.query(Ingredient).filter(
                    Ingredient.name == ingredient_data["name"]
                ).first()
                
                if not ingredient:
                    ingredient = Ingredient(
                        name=ingredient_data["name"],
                        unit=ingredient_data.get("unit")
                    )
                    db.add(ingredient)
                    db.flush()
                
                recipe_ingredient = RecipeIngredient(
                    recipe_id=recipe.recipe_id,
                    ingredient_id=ingredient.ingredient_id,
                    quantity=ingredient_data["quantity"],
                    unit=ingredient_data.get("unit"),
                    note=ingredient_data.get("note")
                )
                db.add(recipe_ingredient)
        
        db.commit()
        db.refresh(recipe)
        return recipe
    
    @staticmethod
    def delete_recipe(db: Session, recipe_id: str) -> bool:
        """
        删除食谱
        
        Args:
            db: 数据库会话
            recipe_id: 食谱ID
        
        Returns:
            是否删除成功
        """
        recipe = RecipeService.get_recipe_by_id(db, recipe_id)
        if not recipe:
            return False
        
        db.delete(recipe)
        db.commit()
        return True
    
    @staticmethod
    def favorite_recipe(db: Session, user_id: str, recipe_id: str) -> Optional[Favorite]:
        """
        收藏食谱
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            recipe_id: 食谱ID
        
        Returns:
            创建的收藏记录，如果已收藏则返回None
        """
        # 检查是否已收藏
        existing = db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.recipe_id == recipe_id
        ).first()
        
        if existing:
            return None
        
        # 创建收藏记录
        favorite = Favorite(
            user_id=user_id,
            recipe_id=recipe_id
        )
        
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        return favorite
    
    @staticmethod
    def unfavorite_recipe(db: Session, user_id: str, recipe_id: str) -> bool:
        """
        取消收藏
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            recipe_id: 食谱ID
        
        Returns:
            是否取消成功
        """
        favorite = db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.recipe_id == recipe_id
        ).first()
        
        if not favorite:
            return False
        
        db.delete(favorite)
        db.commit()
        return True
    
    @staticmethod
    def rate_recipe(db: Session, user_id: str, recipe_id: str, score: int, comment: Optional[str] = None) -> Rating:
        """
        评分食谱
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            recipe_id: 食谱ID
            score: 评分
            comment: 评论
        
        Returns:
            创建或更新的评分记录
        """
        # 查找现有评分
        rating = db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.recipe_id == recipe_id
        ).first()
        
        if rating:
            # 更新现有评分
            rating.score = score
            rating.comment = comment
        else:
            # 创建新评分
            rating = Rating(
                user_id=user_id,
                recipe_id=recipe_id,
                score=score,
                comment=comment
            )
            db.add(rating)
        
        db.commit()
        db.refresh(rating)
        return rating
    
    @staticmethod
    def get_user_favorites(db: Session, user_id: str, skip: int = 0, limit: int = 20) -> List[Favorite]:
        """
        获取用户收藏列表
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            skip: 跳过的记录数
            limit: 返回的记录数
        
        Returns:
            收藏列表
        """
        return db.query(Favorite).options(
            joinedload(Favorite.recipe).joinedload(Recipe.author)
        ).filter(
            Favorite.user_id == user_id
        ).order_by(Favorite.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_recipe_ratings(db: Session, recipe_id: str, skip: int = 0, limit: int = 20) -> List[Rating]:
        """
        获取食谱评分列表
        
        Args:
            db: 数据库会话
            recipe_id: 食谱ID
            skip: 跳过的记录数
            limit: 返回的记录数
        
        Returns:
            评分列表
        """
        return db.query(Rating).options(
            joinedload(Rating.user)
        ).filter(
            Rating.recipe_id == recipe_id
        ).order_by(Rating.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_average_rating(db: Session, recipe_id: str) -> Optional[float]:
        """
        获取食谱平均评分
        
        Args:
            db: 数据库会话
            recipe_id: 食谱ID
        
        Returns:
            平均评分，如果没有评分则返回None
        """
        result = db.query(func.avg(Rating.score)).filter(
            Rating.recipe_id == recipe_id
        ).scalar()
        
        return float(result) if result else None