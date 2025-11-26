# -*- coding: utf-8 -*-
"""
检查nutrition_info表的结构
"""

from app.core.database import engine, Base
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_nutrition_info_table():
    """
    检查nutrition_info表的结构
    """
    try:
        # 创建inspector对象
        inspector = inspect(engine)
        
        # 获取nutrition_info表的列信息
        columns = inspector.get_columns('nutrition_info')
        
        logger.info(f"nutrition_info表的列信息：")
        for column in columns:
            logger.info(f"- {column['name']}: {column['type']} (nullable: {column['nullable']})")
        
        return columns
        
    except Exception as e:
        logger.error(f"检查nutrition_info表时出错：{str(e)}")
        raise


if __name__ == "__main__":
    logger.info("开始检查nutrition_info表结构...")
    check_nutrition_info_table()
    logger.info("检查完成！")
