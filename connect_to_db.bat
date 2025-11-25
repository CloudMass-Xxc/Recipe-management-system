@echo off
echo 正在连接到PostgreSQL数据库...
set PGPASSWORD=xxc1018
psql -U app_user -d recipe_system -c "SET search_path TO app_schema, public; \dt; SELECT '连接成功!' AS status;"
psql -U app_user -d recipe_system
pause