-- 为nutrition_info表添加缺失的字段
ALTER TABLE nutrition_info ADD COLUMN calories DECIMAL(10,2);
ALTER TABLE nutrition_info ADD COLUMN protein DECIMAL(10,2);
ALTER TABLE nutrition_info ADD COLUMN carbs DECIMAL(10,2);
ALTER TABLE nutrition_info ADD COLUMN fat DECIMAL(10,2);