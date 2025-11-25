-- 添加缺失的phone和display_name字段到users表

-- 检查并添加phone字段
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'phone'
    ) THEN
        ALTER TABLE users ADD COLUMN phone character varying(20);
        RAISE NOTICE '已添加phone字段';
    ELSE
        RAISE NOTICE 'phone字段已存在';
    END IF;
END $$;

-- 检查并添加display_name字段
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'display_name'
    ) THEN
        ALTER TABLE users ADD COLUMN display_name character varying(100);
        RAISE NOTICE '已添加display_name字段';
    ELSE
        RAISE NOTICE 'display_name字段已存在';
    END IF;
END $$;

-- 验证字段是否添加成功
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'users'
ORDER BY ordinal_position;
