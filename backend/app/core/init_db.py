from app.core.database import engine, Base
from app.models import *  # 导入所有模型
import logging

logger = logging.getLogger(__name__)

def init_db(drop_existing=False):
    """
    初始化数据库，创建所有表
    
    Args:
        drop_existing: 是否在创建表之前删除所有已存在的表
    """
    try:
        if drop_existing:
            # 删除所有表（仅用于开发环境）
            logger.info("正在删除所有已存在的表...")
            Base.metadata.drop_all(bind=engine)
            logger.info("所有表删除成功")
        
        # 创建所有表
        logger.info("正在创建数据库表...")
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
        return True
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # 在开发环境中，我们可以使用drop_existing=True来强制更新表结构
    init_db(drop_existing=True)