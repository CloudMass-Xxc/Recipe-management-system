# 个性化食谱管理系统 - PostgreSQL数据库配置指南

## 1. 文档概述

本文档详细描述如何在已安装PostgreSQL的系统上配置个性化食谱管理系统所需的数据库环境，包括数据库创建、用户管理、表结构设置、索引创建、性能优化等内容。

## 2. PostgreSQL基础配置

### 2.1 确认PostgreSQL安装状态

首先，确认PostgreSQL已正确安装并正在运行：

```bash
# 检查PostgreSQL版本
psql --version

# 检查PostgreSQL服务状态（Windows）
net start | findstr /i postgresql

# 检查PostgreSQL服务状态（Linux）
systemctl status postgresql
```

### 2.2 连接到PostgreSQL

使用postgres超级用户连接到PostgreSQL：

```bash
# Windows系统
psql -U postgres

# Linux系统
sudo -u postgres psql
```

## 3. 数据库和用户创建

### 3.1 创建项目数据库

```sql
-- 创建数据库
CREATE DATABASE recipe_system;

-- 确认数据库创建成功
\l
```

### 3.2 创建项目用户

```sql
-- 创建应用用户
CREATE USER app_user WITH PASSWORD 'app_password';

-- 授予用户对数据库的所有权限
GRANT ALL PRIVILEGES ON DATABASE recipe_system TO app_user;

-- 确认用户创建成功
\du
```

### 3.3 连接到新创建的数据库

```bash
# 使用新创建的用户连接到数据库
psql -U app_user -d recipe_system
```

## 4. 安装必要的扩展

项目需要使用UUID和其他扩展功能：

```sql
-- 连接到recipe_system数据库
\c recipe_system

-- 创建UUID扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建pgcrypto扩展（用于加密功能）
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 确认扩展安装成功
\dx
```

## 5. 表结构创建

### 5.1 创建users表

> 注意：创建此表前，请确保已按照第4章的说明安装了"uuid-ossp"扩展

```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    diet_preferences JSONB DEFAULT '{}',
    is_active VARCHAR(1) DEFAULT 'Y',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建更新时间触发器函数
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为users表创建更新时间触发器
CREATE TRIGGER update_users_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
```

### 5.2 创建recipes表

> 注意：创建此表前，请确保已按照第4章的说明安装了"uuid-ossp"扩展

```sql
CREATE TABLE recipes (
    recipe_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    ingredients JSONB NOT NULL,
    steps JSONB NOT NULL,
    cooking_time INTEGER,
    difficulty VARCHAR(50),
    nutrition_info JSONB,
    image_url VARCHAR(500),
    tags JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 为recipes表创建更新时间触发器
CREATE TRIGGER update_recipes_timestamp
BEFORE UPDATE ON recipes
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
```

### 5.3 创建ingredients表

```sql
CREATE TABLE ingredients (
    ingredient_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    unit VARCHAR(50),
    nutrition_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5.4 创建recipe_ingredients表

```sql
CREATE TABLE recipe_ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id UUID NOT NULL REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    quantity DECIMAL(10,2) NOT NULL,
    unit VARCHAR(50) NOT NULL
);
```

### 5.5 创建favorites表

```sql
CREATE TABLE favorites (
    favorite_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    recipe_id UUID NOT NULL REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5.6 创建ratings表

```sql
CREATE TABLE ratings (
    rating_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    recipe_id UUID NOT NULL REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    score INTEGER NOT NULL CHECK (score >= 1 AND score <= 5),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5.7 创建nutrition_info表

```sql
CREATE TABLE nutrition_info (
    nutrition_id SERIAL PRIMARY KEY,
    calories DECIMAL(10,2),
    protein DECIMAL(10,2),
    carbs DECIMAL(10,2),
    fat DECIMAL(10,2),
    fiber DECIMAL(10,2),
    vitamins JSONB DEFAULT '{}',
    minerals JSONB DEFAULT '{}'
);
```

### 5.8 创建diet_plans表

```sql
CREATE TABLE diet_plans (
    plan_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    recipes JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 为diet_plans表创建更新时间触发器
CREATE TRIGGER update_diet_plans_timestamp
BEFORE UPDATE ON diet_plans
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
```

## 6. 索引创建

### 6.1 为常用查询字段创建索引

```sql
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
```

### 6.2 创建全文搜索索引

```sql
-- 注意：请确保先创建了recipes表（参考5.2节），然后再执行以下索引创建语句
-- 为食谱标题和描述创建全文搜索索引（使用simple配置替代chinese配置）
CREATE INDEX idx_recipes_search ON recipes USING gin(to_tsvector('simple', title || ' ' || description));

-- 注意：请确保先创建了ingredients表（参考5.3节），然后再执行以下索引创建语句
-- 为食材名称创建全文搜索索引（使用simple配置替代chinese配置）
CREATE INDEX idx_ingredients_search ON ingredients USING gin(to_tsvector('simple', name));
```

### 6.3 创建JSON字段索引

```sql
-- 为食谱标签创建GIN索引
CREATE INDEX idx_recipes_tags ON recipes USING gin(tags);

-- 为用户饮食偏好创建GIN索引
CREATE INDEX idx_users_preferences ON users USING gin(diet_preferences);

-- 为食谱食材创建GIN索引
CREATE INDEX idx_recipes_ingredients_json ON recipes USING gin(ingredients);
```

### 6.4 创建复合唯一索引

```sql
-- 确保用户对同一食谱只能有一个收藏
CREATE UNIQUE INDEX idx_favorites_user_recipe ON favorites(user_id, recipe_id);

-- 确保用户对同一食谱只能有一个评分
CREATE UNIQUE INDEX idx_ratings_user_recipe ON ratings(user_id, recipe_id);

-- 为食谱查询优化创建复合索引
CREATE INDEX idx_recipes_difficulty_time ON recipes(difficulty, cooking_time);
```

## 7. 权限配置

### 7.1 分配最小权限

```sql
-- 连接到PostgreSQL（使用postgres用户）
\c postgres

-- 撤销不必要的权限
REVOKE ALL PRIVILEGES ON SCHEMA public FROM public;

-- 为app_user授予必要的权限
GRANT USAGE ON SCHEMA public TO app_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- 设置默认权限，确保未来创建的表也有正确的权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO app_user;
```

### 7.2 创建只读用户（可选）

如果需要一个只读用户用于报表或数据分析：

```sql
-- 创建只读用户
CREATE USER readonly_user WITH PASSWORD 'readonly_password';

-- 授予只读权限
GRANT CONNECT ON DATABASE recipe_system TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_user;
```

## 8. PostgreSQL配置文件优化

### 8.1 定位配置文件

```bash
# 查找postgresql.conf文件位置（Linux）
find / -name "postgresql.conf" 2>/dev/null

# Windows系统通常位于
# C:\Program Files\PostgreSQL\15\data\postgresql.conf
```

### 8.2 主要配置参数优化

编辑postgresql.conf文件，调整以下参数：

```ini
# 内存配置
shared_buffers = 256MB            # 建议设置为系统内存的25%
work_mem = 16MB                   # 复杂查询的工作内存
maintenance_work_mem = 64MB       # 维护操作（VACUUM等）的内存

# 查询优化
effective_cache_size = 768MB      # 建议设置为系统内存的75%
random_page_cost = 4              # 随机读取成本估计

# 写入性能
wal_buffers = 16MB                # WAL缓冲区大小
checkpoint_completion_target = 0.9 # 检查点完成目标

# 连接数
max_connections = 100             # 最大并发连接数

# 统计信息
autovacuum = on                   # 自动清理

# 日志设置
log_statement = 'ddl'             # 记录DDL语句
log_min_duration_statement = 1000 # 记录执行时间超过1秒的语句
```

### 8.3 重启PostgreSQL应用配置

```bash
# Windows系统
net stop postgresql-x64-15
net start postgresql-x64-15

# Linux系统
sudo systemctl restart postgresql
```

## 9. 连接池配置

### 9.1 安装PgBouncer（可选）

对于高并发应用，建议使用连接池：

```bash
# Ubuntu/Debian
apt-get install pgbouncer

# CentOS/RHEL
yum install pgbouncer

# Windows用户可以从官网下载安装包
```

### 9.2 配置PgBouncer

编辑pgbouncer.ini文件：

```ini
[databases]
recipe_system = host=localhost port=5432 dbname=recipe_system

[pgbouncer]
listen_addr = *
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
default_pool_size = 20
max_client_conn = 100
```

## 10. 数据库连接配置

### 10.1 应用连接字符串

在应用中使用以下连接字符串：

```
postgresql://app_user:app_password@localhost:5432/recipe_system
```

### 10.2 Prisma配置示例

如果使用Prisma ORM，在项目根目录创建schema.prisma文件：

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  user_id           String    @id @default(uuid()) @db.Uuid
  username          String    @unique @db.VarChar(100)
  email             String    @unique @db.VarChar(255)
  password_hash     String    @db.VarChar(255)
  diet_preferences  Json?     @default({})
  is_active         String    @default("Y") @db.Char(1)
  created_at        DateTime  @default(now()) @db.Timestamptz
  updated_at        DateTime  @default(now()) @updatedAt @db.Timestamptz
  favorites         Favorite[]
  ratings           Rating[]
  diet_plans        DietPlan[]
}

model Recipe {
  recipe_id        String        @id @default(uuid()) @db.Uuid
  title            String        @db.VarChar(255)
  description      String?       @db.Text
  ingredients      Json          @default([])
  steps            Json          @default([])
  cooking_time     Int?
  difficulty       String?       @db.VarChar(50)
  nutrition_info   Json?         @default({})
  image_url        String?       @db.VarChar(500)
  tags             Json          @default([])
  created_at       DateTime      @default(now()) @db.Timestamptz
  updated_at       DateTime      @default(now()) @updatedAt @db.Timestamptz
  favorites        Favorite[]
  ratings          Rating[]
  recipe_ingredients RecipeIngredient[]
}

// 其他模型定义...
```

然后在.env文件中设置数据库连接：

```
DATABASE_URL="postgresql://app_user:app_password@localhost:5432/recipe_system"
```

## 11. 备份与恢复策略

### 11.1 创建备份脚本

```bash
#!/bin/bash

# 备份脚本 - backup_db.sh
BACKUP_DIR="/path/to/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/recipe_system_backup_${TIMESTAMP}.sql.gz"

# 创建备份目录
mkdir -p "${BACKUP_DIR}"

# 执行备份
pg_dump -U app_user -d recipe_system | gzip > "${BACKUP_FILE}"

echo "备份完成: ${BACKUP_FILE}"

# 保留最近30天的备份
find "${BACKUP_DIR}" -name "recipe_system_backup_*.sql.gz" -mtime +30 -delete
```

### 11.2 设置定时备份

```bash
# Linux系统 - 添加到crontab
crontab -e

# 添加以下行以每天凌晨2点执行备份
0 2 * * * /path/to/backup_db.sh >> /path/to/backup.log 2>&1

# Windows系统 - 使用任务计划程序创建定时任务
```

### 11.3 恢复数据库

```bash
# 从备份恢复数据库
gunzip -c /path/to/backups/recipe_system_backup_YYYYMMDD_HHMMSS.sql.gz | psql -U app_user -d recipe_system
```

## 12. 性能监控

### 12.1 启用慢查询日志

在postgresql.conf中添加：

```ini
log_min_duration_statement = 1000  # 记录执行时间超过1秒的查询
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '  # 日志格式
```

### 12.2 使用pg_stat_statements扩展

```sql
-- 启用pg_stat_statements扩展
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- 在postgresql.conf中添加
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all
```

### 12.3 监控查询性能

```sql
-- 查看最慢的查询
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

## 13. 常见问题与故障排除

### 13.1 连接问题

- 检查PostgreSQL服务是否运行
- 确认防火墙允许5432端口访问
- 验证用户名和密码是否正确
- 检查pg_hba.conf文件中的访问控制设置

### 13.2 性能问题

- 使用EXPLAIN分析慢查询执行计划
- 检查是否缺少必要的索引
- 考虑增加shared_buffers等内存参数
- 定期运行VACUUM和ANALYZE

### 13.3 存储空间问题

- 监控数据库大小：`SELECT pg_size_pretty(pg_database_size('recipe_system'));`
- 定期清理不需要的数据
- 考虑对大表进行分区

## 14. 总结

本文档提供了个性化食谱管理系统的PostgreSQL数据库详细配置指南。通过按照本文档的步骤操作，您可以成功配置一个结构完整、性能优化、安全可靠的PostgreSQL数据库环境。

关键要点包括：

1. 数据库和用户的正确创建
2. 必要扩展的安装
3. 完整表结构的实现
4. 优化索引的创建
5. 合理的权限配置
6. 性能参数的优化
7. 备份和恢复策略的建立
8. 性能监控的配置

这些配置将确保您的数据库系统能够高效地支持个性化食谱管理系统的运行需求。