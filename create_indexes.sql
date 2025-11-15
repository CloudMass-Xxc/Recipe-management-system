SET search_path TO app_schema, public;

-- 为users表创建索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- 为recipes表创建索引
CREATE INDEX idx_recipes_title ON recipes(title);
CREATE INDEX idx_recipes_difficulty ON recipes(difficulty);

-- 为ingredients表创建索引
CREATE INDEX idx_ingredients_name ON ingredients(name);
CREATE INDEX idx_ingredients_category ON ingredients(category);

-- 为外键字段创建索引
CREATE INDEX idx_favorites_user_id ON favorites(user_id);
CREATE INDEX idx_favorites_recipe_id ON favorites(recipe_id);
CREATE INDEX idx_ratings_user_id ON ratings(user_id);
CREATE INDEX idx_ratings_recipe_id ON ratings(recipe_id);
CREATE INDEX idx_diet_plans_user_id ON diet_plans(user_id);
CREATE INDEX idx_recipe_ingredients_recipe_id ON recipe_ingredients(recipe_id);
CREATE INDEX idx_recipe_ingredients_ingredient_id ON recipe_ingredients(ingredient_id);

-- 创建全文搜索索引
CREATE INDEX idx_recipes_search ON recipes USING gin(to_tsvector('simple', title || ' ' || coalesce(description, '')));
CREATE INDEX idx_ingredients_search ON ingredients USING gin(to_tsvector('simple', name));

-- 创建JSON字段索引
CREATE INDEX idx_recipes_tags ON recipes USING gin(tags);
CREATE INDEX idx_users_preferences ON users USING gin(diet_preferences);
CREATE INDEX idx_recipes_ingredients_json ON recipes USING gin(ingredients);

-- 创建复合唯一索引
CREATE UNIQUE INDEX idx_favorites_user_recipe ON favorites(user_id, recipe_id);
CREATE UNIQUE INDEX idx_ratings_user_recipe ON ratings(user_id, recipe_id);

-- 为食谱查询优化创建复合索引
CREATE INDEX idx_recipes_difficulty_time ON recipes(difficulty, cooking_time);