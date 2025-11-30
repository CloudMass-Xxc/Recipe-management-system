from fastapi import Depends
from app.auth.jwt import get_current_user, get_current_active_user, get_current_superuser
from app.models.user import User

# 重新导出JWT模块中的依赖项，保持API兼容性
# 这些依赖项现在直接从jwt.py导入，因为我们已经在那里实现了所有增强的安全检查
