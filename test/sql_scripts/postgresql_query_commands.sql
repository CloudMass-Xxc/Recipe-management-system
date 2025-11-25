-- PostgreSQL数据库查询常用语句

-- 1. 查询PostgreSQL中所有数据库
-- 方法1: 使用标准SQL查询系统表
SELECT datname FROM pg_database;

-- 方法2: 使用psql元命令（在psql命令行中执行）
-- \l

-- 2. 查询当前连接的数据库
SELECT current_database();

-- 3. 查询数据库大小和使用情况
-- 查询所有数据库的大小
SELECT 
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size,
    pg_database_size(pg_database.datname) AS size_bytes
FROM pg_database
ORDER BY pg_database_size(pg_database.datname) DESC;

-- 4. 查询数据库中所有表（当前数据库）
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;

-- 5. 查询数据库用户
SELECT usename FROM pg_user;

-- 6. 查询数据库活动连接
SELECT 
    datname,
    usename,
    application_name,
    client_addr,
    state,
    query_start
FROM pg_stat_activity;

-- 7. 查询数据库版本
SELECT version();

-- 8. 查询数据库运行状态
SELECT pg_is_in_recovery();

-- 9. 查询数据库表空间
SELECT spcname FROM pg_tablespace;

-- 10. 查询数据库配置参数
SELECT name, setting FROM pg_settings LIMIT 20;