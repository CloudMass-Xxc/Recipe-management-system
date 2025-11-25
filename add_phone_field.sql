-- 为users表添加phone字段
ALTER TABLE users
ADD COLUMN phone VARCHAR(20) UNIQUE;

-- 创建索引以提高查询性能
CREATE INDEX idx_users_phone ON users(phone);

-- 给现有用户添加一些示例手机号数据（可选）
UPDATE users
SET phone = '13800138000' || (ROW_NUMBER() OVER (ORDER BY created_at) % 1000)
WHERE phone IS NULL;

-- 显示添加字段后的表结构
\d users;

-- 显示前5个用户的phone字段值
SELECT user_id, username, phone FROM users LIMIT 5;
