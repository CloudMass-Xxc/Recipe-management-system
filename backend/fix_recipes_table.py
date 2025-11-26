from sqlalchemy import create_engine, text
from app.core.config import settings

# 创建数据库连接
engine = create_engine(settings.DATABASE_URL)
print('数据库连接成功')

with engine.connect() as conn:
    # 检查recipes表是否缺少author_id字段
    result = conn.execute(
        text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'app_schema' AND table_name = 'recipes' AND column_name = 'author_id'")
    )
    
    if result.fetchone():
        print('author_id字段已存在')
    else:
        print('添加author_id字段...')
        # 添加author_id字段
        conn.execute(
            text("ALTER TABLE app_schema.recipes ADD COLUMN author_id UUID REFERENCES app_schema.users(user_id) ON DELETE CASCADE")
        )
        conn.commit()
        print('author_id字段添加成功')
        
        # 再次检查
        result = conn.execute(
            text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'app_schema' AND table_name = 'recipes' AND column_name = 'author_id'")
        )
        print('检查结果:', result.fetchone())
    
    # 检查instructions字段
    result = conn.execute(
        text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'app_schema' AND table_name = 'recipes' AND column_name = 'instructions'")
    )
    
    if result.fetchone():
        print('instructions字段已存在')
    else:
        print('添加instructions字段...')
        conn.execute(
            text("ALTER TABLE app_schema.recipes ADD COLUMN instructions TEXT NOT NULL DEFAULT ''")
        )
        conn.commit()
        print('instructions字段添加成功')
    
    # 检查servings字段
    result = conn.execute(
        text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'app_schema' AND table_name = 'recipes' AND column_name = 'servings'")
    )
    
    if result.fetchone():
        print('servings字段已存在')
    else:
        print('添加servings字段...')
        conn.execute(
            text("ALTER TABLE app_schema.recipes ADD COLUMN servings INTEGER NOT NULL DEFAULT 1")
        )
        conn.commit()
        print('servings字段添加成功')
        
    # 显示更新后的表结构
    print('\n更新后的Recipes表结构:')
    result = conn.execute(
        text("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'app_schema' AND table_name = 'recipes'")
    )
    for row in result.fetchall():
        print(f'列名: {row[0]}, 数据类型: {row[1]}')