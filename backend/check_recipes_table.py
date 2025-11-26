from sqlalchemy import create_engine, text
from app.core.config import settings

# 创建数据库连接
engine = create_engine(settings.DATABASE_URL)
print('数据库连接成功')

with engine.connect() as conn:
    # 只检查列名
    result = conn.execute(
        text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'app_schema' AND table_name = 'recipes' ORDER BY ordinal_position")
    )
    
    column_names = [row[0] for row in result.fetchall()]
    print('Recipes表所有列名:', column_names)
    print('总列数:', len(column_names))
    
    # 检查是否存在steps字段
    if 'steps' in column_names:
        print('发现steps字段!')
    else:
        print('未发现steps字段')
    
    # 检查是否存在instructions字段
    if 'instructions' in column_names:
        print('发现instructions字段')
    else:
        print('未发现instructions字段')
