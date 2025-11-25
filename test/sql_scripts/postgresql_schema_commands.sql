-- PostgreSQL Schema管理和查询命令

-- 1. 查询PostgreSQL中的所有schema
SELECT schema_name FROM information_schema.schemata;

-- 2. 查看当前search_path（影响默认schema的查找顺序）
SHOW search_path;

-- 3. 设置search_path来进入特定schema（方法1）
-- 这会临时改变当前会话的默认schema查找顺序
SET search_path TO app_schema, public;

-- 4. 在查询时显式指定schema（方法2）
-- SELECT * FROM app_schema.users;

-- 5. 创建新的schema（如果需要）
-- CREATE SCHEMA app_schema;

-- 6. 检查特定schema（如app_schema）是否存在
SELECT EXISTS(
    SELECT schema_name 
    FROM information_schema.schemata 
    WHERE schema_name = 'app_schema'
);

-- 7. 列出特定schema中的所有表
-- 将'app_schema'替换为实际的schema名称
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'app_schema';

-- 8. 授予用户对schema的权限
-- GRANT USAGE ON SCHEMA app_schema TO app_user;
-- GRANT ALL ON ALL TABLES IN SCHEMA app_schema TO app_user;

-- 9. 永久修改用户的默认search_path（需要超级用户权限）
-- ALTER USER app_user SET search_path TO app_schema, public;