import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# 从环境变量或.env文件获取数据库连接信息
def get_db_connection_string():
    # 首先尝试从.env文件读取
    try:
        with open('backend/.env', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('DATABASE_URL='):
                    return line.split('=', 1)[1].strip().strip('"')
    except Exception:
        pass
    
    # 返回默认连接字符串
    return "postgresql://app_user:xxc1018@localhost:5432/recipe_system"

def clear_database():
    print("开始清空数据库数据...")
    
    # 获取数据库连接字符串
    db_url = get_db_connection_string()
    print(f"使用数据库连接: {db_url}")
    
    try:
        # 创建数据库引擎
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            # 开始事务
            transaction = connection.begin()
            
            try:
                # 获取所有表名
                print("获取所有表名...")
                result = connection.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name
                """))
                
                tables = [row[0] for row in result]
                print(f"找到 {len(tables)} 个表:", tables)
                
                # 禁用外键约束
                print("禁用外键约束...")
                connection.execute(text("SET CONSTRAINTS ALL DEFERRED"))
                connection.execute(text("ALTER TABLE IF EXISTS alembic_version DISABLE TRIGGER ALL"))
                
                # 清空每个表的数据
                for table in tables:
                    # 跳过系统表
                    if table.startswith('pg_') or table == 'alembic_version':
                        print(f"跳过系统表: {table}")
                        continue
                    
                    print(f"清空表: {table}")
                    try:
                        connection.execute(text(f"DELETE FROM {table}"))
                    except Exception as e:
                        print(f"清空表 {table} 时出错: {e}")
                        # 尝试TRUNCATE
                        try:
                            connection.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
                            print(f"使用TRUNCATE成功清空表: {table}")
                        except Exception as e2:
                            print(f"TRUNCATE表 {table} 也失败: {e2}")
                
                # 重新启用外键约束
                print("重新启用外键约束...")
                connection.execute(text("ALTER TABLE IF EXISTS alembic_version ENABLE TRIGGER ALL"))
                connection.execute(text("SET CONSTRAINTS ALL IMMEDIATE"))
                
                # 提交事务
                transaction.commit()
                print("✅ 数据库数据清空成功！")
                
            except Exception as e:
                # 回滚事务
                transaction.rollback()
                print(f"❌ 清空数据库时发生错误，事务已回滚: {e}")
                raise
                
    except SQLAlchemyError as e:
        print(f"❌ 数据库连接或操作失败: {e}")
    except Exception as e:
        print(f"❌ 程序执行失败: {e}")

if __name__ == "__main__":
    clear_database()