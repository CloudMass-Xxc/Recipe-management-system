from app.core.database import engine
from sqlalchemy import text

try:
    # 测试数据库连接
    with engine.connect() as conn:
        print('数据库连接成功')
        
        # 查询用户表结构
        result = conn.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND table_schema = 'app_schema'
        """))
        
        print('用户表结构:')
        for row in result:
            print(f"列名: {row[0]}, 数据类型: {row[1]}")
            
        # 查询是否存在failed_login_attempts和locked_until字段
        print('\n检查安全相关字段:')
        security_fields = ['failed_login_attempts', 'locked_until']
        for field in security_fields:
            result = conn.execute(text("""
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'users' AND table_schema = 'app_schema' 
                AND column_name = :field_name
            """), {"field_name": field})
            exists = result.fetchone() is not None
            print(f"字段 {field}: {'存在' if exists else '不存在'}")
            
        # 检查schema是否正确
        print('\n检查schema:')
        result = conn.execute(text("""
            SELECT schema_name FROM information_schema.schemata 
            WHERE schema_name = 'app_schema'
        """))
        schema_exists = result.fetchone() is not None
        print(f"Schema 'app_schema': {'存在' if schema_exists else '不存在'}")
        
except Exception as e:
    print(f"数据库操作失败: {str(e)}")