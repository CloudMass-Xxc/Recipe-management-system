-- 先检查用户表
\dt
\d users

-- 查看当前用户数据
SELECT COUNT(*) FROM users;
SELECT user_id, username, email FROM users LIMIT 5;

-- 使用TRUNCATE命令清空用户表，同时级联删除相关数据
TRUNCATE TABLE users CASCADE;

-- 验证数据是否已清空
SELECT COUNT(*) FROM users;
