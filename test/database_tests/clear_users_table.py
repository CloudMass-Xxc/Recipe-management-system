import os
from sqlalchemy import create_engine, text

# 从环境变量或.env文件获取数据库连接信息
def get_db_connection_string():
    try:
        with open('backend/.env', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('DATABASE_URL='):
                    return line.split('=', 1)[1].strip().strip('"')
    except Exception:
        pass
    
    return "postgresql://app_user:xxc1018@localhost:5432/recipe_system"

def clear_users_table():
    print("开始清空用户表数据...")
    
    db_url = get_db_connection_string()
    print(f"使用数据库连接: {db_url}")
    
    try:
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            # 开始事务
            transaction = connection.begin()
            
            try:
                # 清空用户表
                print("清空 app_schema.users 表...")
                
                # 先检查是否有外键约束阻止删除
                print("检查外键约束...")
                fk_result = connection.execute(text("""
                    SELECT tc.table_name, kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = 'app_schema'
                """))
                
                foreign_keys = list(fk_result)
                if foreign_keys:
                    print(f"发现 {len(foreign_keys)} 个外键约束:")
                    for fk in foreign_keys:
                        print(f"  - 表 {fk[0]}.{fk[1]} 引用 {fk[2]}.{fk[3]}")
                    
                    # 禁用外键检查
                    print("临时禁用外键检查...")
                    connection.execute(text("SET session_replication_role = replica"))
                
                # 尝试DELETE方式
                try:
                    delete_result = connection.execute(text("DELETE FROM app_schema.users"))
                    deleted_count = delete_result.rowcount
                    print(f"成功删除 {deleted_count} 条用户记录")
                except Exception as e:
                    print(f"DELETE操作失败: {e}")
                    # 尝试TRUNCATE方式
                    try:
                        print("尝试使用TRUNCATE...")
                        truncate_result = connection.execute(text("TRUNCATE TABLE app_schema.users CASCADE"))
                        print("使用TRUNCATE成功清空用户表")
                    except Exception as e2:
                        print(f"TRUNCATE操作也失败: {e2}")
                        raise
                
                # 恢复外键检查
                if foreign_keys:
                    print("恢复外键检查...")
                    connection.execute(text("SET session_replication_role = origin"))
                
                # 提交事务
                transaction.commit()
                print("✅ 用户表数据清空成功！")
                
                # 验证清空结果
                count_result = connection.execute(text("SELECT COUNT(*) FROM app_schema.users"))
                remaining_count = count_result.scalar()
                print(f"清空后用户表剩余记录数: {remaining_count}")
                
            except Exception as e:
                # 回滚事务
                transaction.rollback()
                print(f"❌ 清空用户表时发生错误，事务已回滚: {e}")
                
                # 恢复外键检查
                try:
                    connection.execute(text("SET session_replication_role = origin"))
                except:
                    pass
                
                raise
                
    except Exception as e:
        print(f"❌ 程序执行失败: {e}")

if __name__ == "__main__":
    clear_users_table()