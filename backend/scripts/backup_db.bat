@echo off

:: 备份脚本 - backup_db.bat
set BACKUP_DIR=d:\Homework\LLM\Final_assignment\Vers_4\backups

:: 获取当前时间戳 (格式: YYYYMMDD_HHMMSS)
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "TIMESTAMP=%dt:~0,8%_%dt:~8,6%"
set "BACKUP_FILE=%BACKUP_DIR%\recipe_system_backup_%TIMESTAMP%.sql.gz"

:: 创建备份目录
mkdir "%BACKUP_DIR%" 2>nul

:: 执行备份
pg_dump -U app_user -d recipe_system | gzip > "%BACKUP_FILE%"

echo 备份完成: %BACKUP_FILE%

:: Windows下删除30天前的备份文件 (需要PowerShell支持)
powershell -Command "Get-ChildItem -Path '%BACKUP_DIR%' -Filter 'recipe_system_backup_*.sql.gz' | Where-Object {($_.CreationTime -lt (Get-Date).AddDays(-30))} | Remove-Item"