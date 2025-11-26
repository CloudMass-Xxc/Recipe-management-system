from sqlalchemy import create_engine, text
from app.core.config import settings

# 创建数据库连接
engine = create_engine(settings.DATABASE_URL)
print('数据库连接成功')

with engine.connect() as conn:
    # 检查recipe_ingredients表的结构
    print('\n检查recipe_ingredients表结构:')
    result = conn.execute(
        text("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'app_schema' AND table_name = 'recipe_ingredients' ORDER BY ordinal_position")
    )
    
    columns = [(row[0], row[1]) for row in result.fetchall()]
    print('Recipe_ingredients表所有列:')
    for col_name, col_type in columns:
        print(f'  - {col_name}: {col_type}')
    print('总列数:', len(columns))
    
    # 检查是否存在note字段
    if any(col[0] == 'note' for col in columns):
        print('发现note字段!')
    else:
        print('未发现note字段')
