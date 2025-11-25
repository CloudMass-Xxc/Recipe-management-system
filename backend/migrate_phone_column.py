from sqlalchemy import text
from app.core.database import engine

def add_missing_columns():
    try:
        with engine.connect() as conn:
            # 切换到正确的schema
            conn.execute(text("SET search_path TO app_schema"))
            
            # 定义需要添加的字段
            columns_to_add = [
                {"name": "display_name", "type": "VARCHAR(255)", "nullable": False, "default": "''"},
                {"name": "avatar_url", "type": "VARCHAR(500)", "nullable": True},
                {"name": "bio", "type": "TEXT", "nullable": True},
                {"name": "diet_preferences", "type": "JSON", "nullable": True},
                {"name": "is_active", "type": "BOOLEAN", "nullable": True, "default": "true"},
                {"name": "is_superuser", "type": "BOOLEAN", "nullable": True, "default": "false"},
                {"name": "updated_at", "type": "TIMESTAMP WITH TIME ZONE", "nullable": True, "default": "now()"},
            ]
            
            for column in columns_to_add:
                # 检查字段是否存在
                result = conn.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='users' AND column_name='{column['name']}'
                """))
                
                if not result.fetchone():
                    print(f"添加{column['name']}字段到users表...")
                    # 构建ALTER TABLE语句
                    default_clause = f" DEFAULT {column['default']}" if column.get('default') else ""
                    nullable_clause = " NOT NULL" if not column['nullable'] else " NULL"
                    
                    conn.execute(text(f"""
                        ALTER TABLE users 
                        ADD COLUMN {column['name']} {column['type']}{nullable_clause}{default_clause}
                    """))
                    print(f"{column['name']}字段添加成功!")
                else:
                    print(f"{column['name']}字段已存在")
            
            conn.commit()
            print("所有缺失字段添加完成!")
                
    except Exception as e:
        print(f"添加字段时出错: {str(e)}")

if __name__ == "__main__":
    add_missing_columns()