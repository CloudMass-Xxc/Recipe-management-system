-- 检查并添加phone字段到users表
-- 作者: AI Assistant
-- 日期: 当前日期
-- 描述: 检查users表中是否存在phone字段，如果不存在则添加

-- 检查phone字段是否存在
DO $$
BEGIN
    -- 检查字段是否存在
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'users' 
        AND column_name = 'phone'
    ) THEN
        -- 添加phone字段
        ALTER TABLE public.users 
        ADD COLUMN phone VARCHAR(20) UNIQUE NULL;
        
        -- 为phone字段创建索引以加速查询
        CREATE INDEX IF NOT EXISTS idx_users_phone ON public.users(phone);
        
        RAISE NOTICE '成功添加phone字段到users表';
    ELSE
        RAISE NOTICE 'phone字段已存在于users表中，跳过添加操作';
    END IF;
END$$;

-- 验证字段是否添加成功
SELECT 
    column_name, 
    data_type, 
    character_maximum_length, 
    is_nullable
FROM 
    information_schema.columns 
WHERE 
    table_schema = 'public' 
    AND table_name = 'users' 
    AND column_name = 'phone';

-- 显示users表的完整结构以确认更改
SELECT column_name, data_type, character_maximum_length, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
AND table_name = 'users'
ORDER BY ordinal_position;
