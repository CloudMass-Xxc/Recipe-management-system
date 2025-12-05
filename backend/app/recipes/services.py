from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
from uuid import UUID
from typing import List, Optional, Dict, Any
import logging
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.recipe_ingredient import RecipeIngredient
from app.models.nutrition_info import NutritionInfo
from app.models.rating import Rating
from app.models.user import User
from app.core.utils import generate_recipe_id

# 配置日志记录器
logger = logging.getLogger(__name__)

class RecipeService:
    """
    食谱服务类，处理食谱相关的业务逻辑
    """
    
    @staticmethod
    def create_recipe(db: Session, author_id: Any, recipe_data: Dict[str, Any]) -> Recipe:
        """
        创建新食谱
        
        Args:
            db: 数据库会话
            author_id: 作者ID
            recipe_data: 食谱数据
        
        Returns:
            创建的食谱对象
        """
        import json
        from sqlalchemy import text
        
        # 提取营养信息
        nutrition_info = recipe_data.pop("nutrition_info", None)
        
        # 准备创建食谱的数据
        title = recipe_data.get("title", "")
        description = recipe_data.get("description", "")
        instructions = recipe_data.get("instructions", "")
        cooking_time = recipe_data.get("cooking_time", 0)
        servings = recipe_data.get("servings", 1)
        difficulty = recipe_data.get("difficulty", "easy")
        ingredients = recipe_data.get("ingredients", [])
        tags = recipe_data.get("tags", [])
        image_url = recipe_data.get("image_url")
        
        # 转换枚举类型
        if hasattr(difficulty, "value"):
            difficulty = difficulty.value
        
        # 确保ingredients和tags是列表类型
        if ingredients is None:
            ingredients = []
        if tags is None:
            tags = []
        
        # 生成新的recipe_id
        from app.core.utils import generate_recipe_id
        recipe_id = generate_recipe_id()
        
        # 使用参数绑定的方式执行INSERT语句
        # 这样可以确保安全处理JSON数据和所有类型
        insert_query = text("""
        INSERT INTO app_schema.recipes (
            recipe_id, author_id, title, description, instructions, 
            cooking_time, servings, difficulty, ingredients, tags, 
            image_url, steps
        ) VALUES (
            :recipe_id, :author_id, :title, :description, :instructions, 
            :cooking_time, :servings, :difficulty, :ingredients, :tags, 
            :image_url, :steps
        )
        """)
        
        # 将instructions字符串转换为步骤列表的JSON格式
        # 按照换行符分割instructions，创建步骤列表
        steps_list = [step.strip() for step in instructions.split('\n') if step.strip()]
        steps_json = json.dumps(steps_list)
        
        # 执行插入，使用参数绑定
        db.execute(insert_query, {
            "recipe_id": recipe_id,
            "author_id": author_id,
            "title": title,
            "description": description,
            "instructions": instructions,
            "cooking_time": cooking_time,
            "servings": servings,
            "difficulty": difficulty,
            "ingredients": json.dumps(ingredients),  # 转换为JSON字符串
            "tags": json.dumps(tags),  # 转换为JSON字符串
            "image_url": image_url,
            "steps": steps_json  # steps字段使用JSON格式的步骤列表
        })
        
        # 创建营养信息
        if nutrition_info:
            new_nutrition = NutritionInfo(
                recipe_id=recipe_id,
                **nutrition_info
            )
            db.add(new_nutrition)
        
        # 处理食材关联表（如果提供了足够的信息）
        for ingredient_data in ingredients:
            # 检查是否有name字段（确保是完整的食材对象）
            if isinstance(ingredient_data, dict) and "name" in ingredient_data:
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
                    recipe_id=recipe_id,
                    ingredient_id=ingredient.ingredient_id,
                    quantity=ingredient_data.get("quantity", 1),
                    unit=ingredient_data.get("unit")
                )
                db.add(recipe_ingredient)
        
        db.commit()
        
        # 获取并返回创建的食谱对象
        new_recipe = RecipeService.get_recipe_by_id(db, recipe_id)
        return new_recipe
    
    @staticmethod
    def get_recipe_by_id(db: Session, recipe_id: Any, load_relationships: bool = True) -> Optional[Recipe]:
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
        
        # 安全地处理recipe_id，无论它是什么类型
        try:
            if isinstance(recipe_id, UUID):
                # 如果已经是UUID对象，直接使用
                query = query.filter(Recipe.recipe_id == recipe_id)
            else:
                # 否则转换为字符串，然后尝试转换为UUID
                try:
                    recipe_id_uuid = UUID(str(recipe_id))
                    query = query.filter(Recipe.recipe_id == recipe_id_uuid)
                except ValueError:
                    # 如果不是有效UUID格式，直接返回None
                    return None
        except Exception as e:
            # 捕获任何其他可能的异常，返回None
            return None
        
        return query.first()
    
    @staticmethod
    def get_recipes(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        author_id: Optional[Any] = None,
        user_id: Optional[Any] = None,  # 当前用户ID，用于排除已收藏的食谱
        search_params: Optional[Dict[str, Any]] = None
    ) -> List[Recipe]:
        """
        获取食谱列表
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的记录数
            author_id: 作者ID（可选）
            user_id: 当前用户ID（可选），用于排除已收藏的食谱
            search_params: 搜索参数（可选）
        
        Returns:
            食谱列表
        """
        query = db.query(Recipe).options(
            joinedload(Recipe.author)
        )
        
        # 排除当前用户已收藏的食谱
        if user_id:
            from app.models.favorite import Favorite
            from sqlalchemy import not_
            
            try:
                # 安全地处理user_id
                from uuid import UUID
                if isinstance(user_id, UUID):
                    user_id_uuid = user_id
                else:
                    user_id_uuid = UUID(str(user_id))
                
                # 子查询：获取用户已收藏的食谱ID列表
                favorited_recipe_ids = db.query(Favorite.recipe_id).filter(
                    Favorite.user_id == user_id_uuid
                ).subquery()
                
                # 排除已收藏的食谱
                query = query.filter(
                    not_(Recipe.recipe_id.in_(favorited_recipe_ids))
                )
                logger.info(f"成功排除用户ID {user_id} 的已收藏食谱")
            except Exception as e:
                logger.error(f"处理用户收藏过滤时出错: {str(e)}")
                # 如果处理用户ID出错，不影响整体查询，继续执行
        
        # 按作者筛选
        if author_id:
            # 安全地处理author_id
            if isinstance(author_id, UUID):
                query = query.filter(Recipe.author_id == author_id)
            else:
                try:
                    author_id_uuid = UUID(str(author_id))
                    query = query.filter(Recipe.author_id == author_id_uuid)
                except Exception as e:
                    logger.error(f"处理作者ID过滤时出错: {str(e)}")
                    # 如果处理作者ID出错，不影响整体查询，继续执行
        
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
                    # 使用PostgreSQL的JSONB操作符正确查询JSON数组
                    query = query.filter(
                        and_(
                            Recipe.tags.isnot(None),
                            func.jsonb_contains(Recipe.tags, func.to_jsonb([tag]))
                        )
                    )
            
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
    def get_recipes_count(
        db: Session,
        author_id: Optional[Any] = None,
        user_id: Optional[Any] = None,  # 添加user_id参数，用于排除已收藏的食谱
        search_params: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        获取食谱总数
        
        Args:
            db: 数据库会话
            author_id: 作者ID（可选）
            user_id: 当前用户ID（可选），用于排除已收藏的食谱
            search_params: 搜索参数（可选）
        
        Returns:
            食谱总数
        """
        query = db.query(func.count(Recipe.recipe_id))
        
        # 排除当前用户已收藏的食谱
        if user_id:
            from app.models.favorite import Favorite
            from sqlalchemy import not_
            
            try:
                # 安全地处理user_id
                from uuid import UUID
                if isinstance(user_id, UUID):
                    user_id_uuid = user_id
                else:
                    user_id_uuid = UUID(str(user_id))
                
                # 子查询：获取用户已收藏的食谱ID列表
                favorited_recipe_ids = db.query(Favorite.recipe_id).filter(
                    Favorite.user_id == user_id_uuid
                ).subquery()
                
                # 排除已收藏的食谱
                query = query.filter(
                    not_(Recipe.recipe_id.in_(favorited_recipe_ids))
                )
                logger.info(f"成功排除用户ID {user_id} 的已收藏食谱")
            except Exception as e:
                logger.error(f"处理用户收藏过滤时出错: {str(e)}")
                # 如果处理用户ID出错，不影响整体查询，继续执行
        
        # 按作者筛选
        if author_id:
            # 安全地处理author_id
            if isinstance(author_id, UUID):
                query = query.filter(Recipe.author_id == author_id)
            else:
                query = query.filter(Recipe.author_id == UUID(str(author_id)))
        
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
                    # 使用PostgreSQL的JSONB操作符正确查询JSON数组
                    query = query.filter(
                        and_(
                            Recipe.tags.isnot(None),
                            func.jsonb_contains(Recipe.tags, func.to_jsonb([tag]))
                        )
                    )
            
            # 按难度筛选
            if search_params.get("difficulty"):
                query = query.filter(Recipe.difficulty == search_params["difficulty"])
            
            # 按烹饪时间筛选
            if search_params.get("max_cooking_time"):
                query = query.filter(Recipe.cooking_time <= search_params["max_cooking_time"])
        
        return query.scalar() or 0
    
    @staticmethod
    def update_recipe(db: Session, recipe_id: Any, recipe_data: Dict[str, Any]) -> Optional[Recipe]:
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
                    unit=ingredient_data.get("unit")
                )
                db.add(recipe_ingredient)
        
        db.commit()
        db.refresh(recipe)
        return recipe
    
    @staticmethod
    def delete_recipe(db: Session, recipe_id: Any) -> bool:
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
    def rate_recipe(db: Session, user_id: Any, recipe_id: Any, score: int, comment: Optional[str] = None) -> Rating:
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
    def get_recipe_ratings(db: Session, recipe_id: Any, skip: int = 0, limit: int = 20) -> List[Rating]:
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
    def get_average_rating(db: Session, recipe_id: Any) -> Optional[float]:
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
    
    @staticmethod
    def add_favorite(db: Session, user_id: Any, recipe_id: Any) -> Any:
        """
        添加食谱到收藏
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            recipe_id: 食谱ID
        
        Returns:
            收藏对象，如果添加失败则返回None
        """
        from app.models.favorite import Favorite
        from uuid import UUID
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # 检查是否已经收藏
            existing_favorite = db.query(Favorite).filter(
                Favorite.user_id == UUID(str(user_id)),
                Favorite.recipe_id == UUID(str(recipe_id))
            ).first()
            
            if existing_favorite:
                logger.info(f"食谱 {recipe_id} 已被用户 {user_id} 收藏")
                return existing_favorite
            
            # 创建新收藏
            new_favorite = Favorite(
                user_id=UUID(str(user_id)),
                recipe_id=UUID(str(recipe_id))
            )
            
            db.add(new_favorite)
            db.commit()
            db.refresh(new_favorite)
            
            logger.info(f"用户 {user_id} 成功收藏食谱 {recipe_id}")
            return new_favorite
        except Exception as e:
            logger.error(f"添加收藏失败: {str(e)}")
            db.rollback()
            return None
    
    @staticmethod
    def remove_favorite(db: Session, user_id: Any, recipe_id: Any) -> bool:
        """
        从收藏中移除食谱
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            recipe_id: 食谱ID
        
        Returns:
            是否移除成功
        """
        from app.models.favorite import Favorite
        from uuid import UUID
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # 查找收藏记录
            favorite = db.query(Favorite).filter(
                Favorite.user_id == UUID(str(user_id)),
                Favorite.recipe_id == UUID(str(recipe_id))
            ).first()
            
            if not favorite:
                logger.info(f"用户 {user_id} 未收藏食谱 {recipe_id}")
                return False
            
            # 删除收藏记录
            db.delete(favorite)
            db.commit()
            
            logger.info(f"用户 {user_id} 成功取消收藏食谱 {recipe_id}")
            return True
        except Exception as e:
            logger.error(f"取消收藏失败: {str(e)}")
            db.rollback()
            return False
    
    @staticmethod
    def get_user_favorites(db: Session, user_id: Any, skip: int = 0, limit: int = 100) -> List[Any]:
        """
        获取用户的收藏列表
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            skip: 跳过的记录数
            limit: 返回的记录数
        
        Returns:
            收藏列表
        """
        from app.models.favorite import Favorite
        from uuid import UUID
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            # 获取用户收藏列表，包含食谱信息
            favorites = db.query(Favorite).options(
                joinedload(Favorite.recipe).joinedload(Recipe.author)
            ).filter(
                Favorite.user_id == UUID(str(user_id))
            ).order_by(
                Favorite.created_at.desc()
            ).offset(skip).limit(limit).all()
            
            logger.info(f"成功获取用户 {user_id} 的收藏列表，共 {len(favorites)} 条记录")
            return favorites
        except Exception as e:
            logger.error(f"获取用户收藏列表失败: {str(e)}")
            return []
    
    @staticmethod
    def is_favorite(db: Session, user_id: Any, recipe_id: Any) -> bool:
        """
        检查食谱是否已被用户收藏
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            recipe_id: 食谱ID
        
        Returns:
            是否已收藏
        """
        from app.models.favorite import Favorite
        from uuid import UUID
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            favorite = db.query(Favorite).filter(
                Favorite.user_id == UUID(str(user_id)),
                Favorite.recipe_id == UUID(str(recipe_id))
            ).first()
            
            return favorite is not None
        except Exception as e:
            logger.error(f"检查收藏状态失败: {str(e)}")
            return False