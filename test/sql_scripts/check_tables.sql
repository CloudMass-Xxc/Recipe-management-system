-- 检查连接信息
SELECT current_database(), current_user;

-- 设置search_path
SET search_path TO app_schema, public;

-- 列出app_schema中的表
\dt app_schema.*

-- 查询users表
SELECT * FROM app_schema.users;

-- 也可以直接查询
SELECT * FROM users;