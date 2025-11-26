# -*- coding: utf-8 -*-
"""
修复nutrition_info表结构，使其与模型定义一致
"""

from sqlalchemy import inspect, text
from app.core.database import engine, Base
from app.models.nutrition_info import NutritionInfo
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def fix_nutrition_info_table():
    """
    修复nutrition_info表结构
    """
    try:
        logger.info("开始修复nutrition_info表结构...")
        
        with engine.connect() as conn:
            # 检查当前表结构
            logger.info("检查当前表结构...")
            inspector = inspect(engine)
            columns = inspector.get_columns('nutrition_info', schema='app_schema')
            column_names = [col['name'] for col in columns]
            
            logger.info(f"当前nutrition_info表的列: {column_names}")
            
            # 开始事务
            with conn.begin():
                # 添加缺少的列
                if 'recipe_id' not in column_names:
                    logger.info("添加recipe_id列...")
                    conn.execute(text("""
                        ALTER TABLE app_schema.nutrition_info 
                        ADD COLUMN recipe_id UUID REFERENCES app_schema.recipes(recipe_id) ON DELETE CASCADE UNIQUE
                    """))
                
                if 'carbs' not in column_names:
                    logger.info("添加carbs列...")
                    conn.execute(text("""
                        ALTER TABLE app_schema.nutrition_info 
                        ADD COLUMN carbs FLOAT NOT NULL DEFAULT 0
                    """))
                
                if 'sugar' not in column_names:
                    logger.info("添加sugar列...")
                    conn.execute(text("""
                        ALTER TABLE app_schema.nutrition_info 
                        ADD COLUMN sugar FLOAT
                    """))
                
                if 'sodium' not in column_names:
                    logger.info("添加sodium列...")
                    conn.execute(text("""
                        ALTER TABLE app_schema.nutrition_info 
                        ADD COLUMN sodium FLOAT
                    """))
                
                if 'additional_nutrients' not in column_names:
                    logger.info("添加additional_nutrients列...")
                    conn.execute(text("""
                        ALTER TABLE app_schema.nutrition_info 
                        ADD COLUMN additional_nutrients JSON
                    """))
                
                # 删除多余的列（如果存在）
                if 'vitamins' in column_names:
                    logger.info("删除vitamins列...")
                    conn.execute(text("""
                        ALTER TABLE app_schema.nutrition_info 
                        DROP COLUMN vitamins
                    """))
                
                if 'minerals' in column_names:
                    logger.info("删除minerals列...")
                    conn.execute(text("""
                        ALTER TABLE app_schema.nutrition_info 
                        DROP COLUMN minerals
                    """))
            
            logger.info("nutrition_info表结构修复完成！")
            
            # 再次检查表结构
            logger.info("检查修复后的表结构...")
            columns = inspector.get_columns('nutrition_info', schema='app_schema')
            column_names = [col['name'] for col in columns]
            logger.info(f"修复后的nutrition_info表的列: {column_names}")
            
            return True
            
    except Exception as e:
        logger.error(f"修复nutrition_info表结构时出错: {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    logger.info("开始执行nutrition_info表结构修复脚本...")
    success = fix_nutrition_info_table()
    if success:
        logger.info("脚本执行成功！nutrition_info表结构已修复。")
    else:
        logger.error("脚本执行失败！nutrition_info表结构修复失败。")
