import psycopg2
from app.core.config import settings

def add_phone_column():
    # 获取数据库连接字符串并解析
    db_url = settings.DATABASE_URL
    # 从URL中提取连接信息
    import re
    match = re.match(r'postgresql://(.*?):(.*?)@(.*?):(.*?)/(.*?)', db_url)
    if not match:
        print("无法解析数据库URL")
        return
    
    user, password, host, port, dbname = match.groups()
    
    try:
        # 连接数据库
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # 切换到指定的schema
        cursor.execute(f"SET search_path TO {settings.DATABASE_SCHEMA}")
        
        # 检查phone字段是否存在
        cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='phone'"
        )
        
        if not cursor.fetchone():
            print("添加phone字段到users表...")
            # 添加phone字段
            cursor.execute("ALTER TABLE users ADD COLUMN phone VARCHAR(20) NULL")
            print("phone字段添加成功!")
        else:
            print("phone字段已存在")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"添加phone字段时出错: {str(e)}")

if __name__ == "__main__":
    add_phone_column()