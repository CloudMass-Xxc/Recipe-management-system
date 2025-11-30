import sys
import os
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from app.core.database import get_db, engine, Base
from app.models.user import User

# 创建所有表
Base.metadata.create_all(bind=engine)

# 获取数据库会话
db = next(get_db())

print("测试数据来源验证日志...")

# 调用User模型的方法，应该会生成数据来源验证日志
try:
    # 尝试获取一个不存在的用户，这应该会生成数据来源验证日志
    user = User.get_by_id(db, "non-existent-id")
    print(f"获取用户结果: {user}")
    
    # 尝试通过用户名获取用户
    user = User.get_by_username(db, "test-user")
    print(f"获取用户结果: {user}")
    
    print("测试完成，请查看日志输出是否包含[DATA_SOURCE_VERIFICATION]前缀的日志")
except Exception as e:
    print(f"测试过程中发生错误: {e}")
finally:
    # 关闭数据库会话
    db.close()