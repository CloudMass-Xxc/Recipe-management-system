SET search_path TO app_schema, public;

-- 创建更新时间触发器函数
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为users表创建更新时间触发器
CREATE TRIGGER update_users_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- 为recipes表创建更新时间触发器
CREATE TRIGGER update_recipes_timestamp
BEFORE UPDATE ON recipes
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- 为diet_plans表创建更新时间触发器
CREATE TRIGGER update_diet_plans_timestamp
BEFORE UPDATE ON diet_plans
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();