from app.core.database import engine
from sqlalchemy import text
import time

try:
    # 连接数据库
    with engine.connect() as conn:
        print('开始添加缺失的安全相关字段...')
        
        # 添加failed_login_attempts字段
        print('添加 failed_login_attempts 字段...')
        conn.execute(text("""
            ALTER TABLE app_schema.users 
            ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0
        """))
        conn.commit()
        print('failed_login_attempts 字段添加成功')
        
        # 添加locked_until字段
        print('添加 locked_until 字段...')
        conn.execute(text("""
            ALTER TABLE app_schema.users 
            ADD COLUMN IF NOT EXISTS locked_until TIMESTAMP WITH TIME ZONE
        """))
        conn.commit()
        print('locked_until 字段添加成功')
        
        # 验证字段是否已添加
        print('\n验证字段添加结果:')
        security_fields = ['failed_login_attempts', 'locked_until']
        for field in security_fields:
            result = conn.execute(text("""
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'users' AND table_schema = 'app_schema' 
                AND column_name = :field_name
            """), {"field_name": field})
            exists = result.fetchone() is not None
            print(f"字段 {field}: {'成功添加' if exists else '添加失败'}")
        
        print('\n数据库字段更新完成！')
        print('建议重启后端服务以应用更改。')
        
except Exception as e:
    print(f"添加字段失败: {str(e)}")