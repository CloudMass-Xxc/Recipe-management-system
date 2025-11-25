
-- PostgreSQL表访问测试脚本
-- 保存为test_table_access.sql并使用: psql -U 用户名 -d recipe_system -f test_table_access.sql

-- 1. 检查当前连接信息
SELECT current_user AS "当前用户", current_database() AS "当前数据库";

-- 2. 检查search_path
SHOW search_path;

-- 3. 尝试设置search_path
SET search_path TO app_schema, public;
SHOW search_path;

-- 4. 检查表是否存在
SELECT EXISTS(
    SELECT 1 
    FROM information_schema.tables 
    WHERE table_schema = 'app_schema' 
    AND table_name = 'users'
) AS "表是否存在";

-- 5. 在所有schema中搜索users表
SELECT table_schema, table_name 
FROM information_schema.tables 
WHERE LOWER(table_name) = 'users';

-- 6. 尝试查询表（如果存在）
DO $$
BEGIN
    IF EXISTS(
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_schema = 'app_schema' 
        AND table_name = 'users'
    ) THEN
        RAISE NOTICE '尝试查询app_schema.users表...';
        -- 注意：下面的查询会在执行时失败，如果没有权限
        -- 取消注释以测试实际查询
        -- SELECT * FROM app_schema.users LIMIT 1;
    END IF;
END $$;

-- 7. 检查权限
SELECT 
    has_schema_privilege(current_user, 'app_schema', 'USAGE') AS "有USAGE权限",
    has_table_privilege(current_user, 'app_schema.users', 'SELECT') AS "有SELECT权限";
