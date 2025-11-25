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

def clear_database_with_cascade():
    print("开始使用CASCADE方式清空数据库...")
    
    db_url = get_db_connection_string()
    print(f"使用数据库连接: {db_url}")
    
    try:
        engine = create_engine(db_url)
        
        with engine.connect() as connection:
            # 开始事务
            transaction = connection.begin()
            
            try:
                # 按依赖关系顺序删除数据
                print("按依赖关系顺序删除数据...")
                
                # 删除最底层依赖表
                print("\n删除依赖表数据:")
                
                # 定义删除顺序（从最依赖到最少依赖）
                tables_to_clear = [
                    "meal_plan_recipes",  # 依赖meal_plans和recipes
                    "recipe_ingredients",  # 依赖recipes和ingredients
                    "favorites",          # 依赖users和recipes
                    "ratings",            # 依赖users和recipes
                    "user_recipe_interactions",  # 依赖users和recipes
                    "meal_plans",         # 依赖users
                    "diet_plans",         # 依赖users
                    "recipes",            # 主表
                    "ingredients",        # 主表
                    "nutrition_info",     # 主表
                    "users"               # 用户表
                ]
                
                # 统计删除记录数
                total_deleted = 0
                
                for table in tables_to_clear:
                    try:
                        print(f"清空 app_schema.{table} 表...")
                        result = connection.execute(text(f"DELETE FROM app_schema.{table} CASCADE"))
                        deleted_count = result.rowcount
                        total_deleted += deleted_count
                        print(f"  成功删除 {deleted_count} 条记录")
                    except Exception as e:
                        print(f"  清空表 {table} 时出错: {e}")
                
                # 提交事务
                transaction.commit()
                print(f"\n✅ 数据库清空成功！总共删除 {total_deleted} 条记录")
                
                # 验证所有表都已清空
                print("\n验证所有表的清空状态:")
                all_empty = True
                
                for table in tables_to_clear:
                    count_result = connection.execute(text(f"SELECT COUNT(*) FROM app_schema.{table}"))
                    count = count_result.scalar()
                    status = "✅ 已清空" if count == 0 else f"❌ 仍有 {count} 条记录"
                    print(f"  app_schema.{table}: {status}")
                    if count > 0:
                        all_empty = False
                
                if all_empty:
                    print("\n🎉 所有表数据都已成功清空！")
                else:
                    print("\n⚠️  部分表数据未完全清空。")
                    
            except Exception as e:
                # 回滚事务
                transaction.rollback()
                print(f"\n❌ 清空数据库时发生错误，事务已回滚: {e}")
                raise
                
    except Exception as e:
        print(f"\n❌ 程序执行失败: {e}")

if __name__ == "__main__":
    clear_database_with_cascade()