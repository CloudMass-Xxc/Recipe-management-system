-- PostgreSQL表访问修复命令
-- 解决 'ERROR: relation "app_schema.users" does not exist' 问题

-- 问题诊断结果:
-- 1. app_schema.users 表确实存在
-- 2. 用户有正确的访问权限
-- 3. 问题原因: 默认search_path中没有包含app_schema


-- === 方法1: 使用完全限定名 (临时解决方案) ===
-- 每次查询时都明确指定schema
SELECT * FROM app_schema.users;

-- 确认表结构
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'app_schema' 
AND table_name = 'users';


-- === 方法2: 设置临时search_path (当前会话有效) ===
-- 在psql会话中执行此命令，之后可以直接使用表名而无需schema前缀
SET search_path TO app_schema, public;

-- 验证search_path是否已更新
SHOW search_path;

-- 现在可以直接查询，无需schema前缀
SELECT * FROM users;


-- === 方法3: 设置永久search_path (推荐) ===
-- 以管理员身份运行以下命令，为app_user用户永久设置search_path
-- 注意: 需要使用postgres或其他有ALTER USER权限的用户登录
-- ALTER USER app_user SET search_path TO app_schema, public;


-- === 表验证命令 ===
-- 列出app_schema中的所有表
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'app_schema' 
ORDER BY table_name;

-- 检查用户权限
SELECT 
    has_schema_privilege(current_user, 'app_schema', 'USAGE') AS "有USAGE权限",
    has_table_privilege(current_user, 'app_schema.users', 'SELECT') AS "有SELECT权限";


-- === 常见问题解答 ===
/*

Q: 为什么我使用 SELECT * FROM app_schema.users 仍然报错?
A: 可能有以下原因:
   1. 数据库连接字符串中可能没有正确指定database名
   2. 检查用户名和密码是否正确
   3. 确认用户对app_schema有USAGE权限

Q: 如何确认我连接的是正确的数据库?
A: 在psql中执行: \l 列出所有数据库，\c recipe_system 连接到正确的数据库

Q: 如何永久解决这个问题?
A: 使用管理员账户运行 ALTER USER app_user SET search_path TO app_schema, public;

*/

-- === psql命令行示例 ===
/*

方法1 (临时使用完全限定名):
   psql -U app_user -d recipe_system
   SELECT * FROM app_schema.users;

方法2 (设置临时search_path):
   psql -U app_user -d recipe_system
   SET search_path TO app_schema, public;
   SELECT * FROM users;

方法3 (推荐 - 永久设置search_path):
   psql -U postgres
   ALTER USER app_user SET search_path TO app_schema, public;
   \q
   psql -U app_user -d recipe_system
   SELECT * FROM users;

*/