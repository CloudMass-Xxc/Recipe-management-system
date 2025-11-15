#!/usr/bin/env pwsh

# 数据库增量备份脚本
# 配置参数
$DB_HOST = "localhost"
$DB_PORT = "5432"
$DB_NAME = "recipe_system"
$DB_USER = "app_user"
$BACKUP_DIR = "d:/Homework/LLM/Final_assignment/Vers_4/backup/incremental"
$LOG_FILE = "d:/Homework/LLM/Final_assignment/Vers_4/backup/incremental_backup.log"

# 需要增量备份的表
$IMPORTANT_TABLES = @(
    "public.users",
    "public.recipes",
    "public.favorites",
    "public.ratings"
)

# 创建备份目录
if (-not (Test-Path -Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Force -Path $BACKUP_DIR | Out-Null
}

# 记录日志函数
function Write-Log {
    param (
        [string]$Message
    )
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $LOG_FILE -Value "[$Timestamp] $Message"
    Write-Host "[$Timestamp] $Message"
}

# 生成备份文件名
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_FILE = "${BACKUP_DIR}/${DB_NAME}_incremental_${TIMESTAMP}.sql"

# 执行增量备份
Write-Log "开始增量备份数据库: $DB_NAME"
try {
    # 设置密码环境变量
    $env:PGPASSWORD = "app_password"
    
    # 创建备份文件
    New-Item -ItemType File -Path $BACKUP_FILE -Force | Out-Null
    
    # 备份每个重要表
    foreach ($table in $IMPORTANT_TABLES) {
        Write-Log "开始备份表: $table"
        $table_name = $table.Split('.')[1]
        $table_backup = "${BACKUP_DIR}/${table_name}_${TIMESTAMP}.sql"
        
        # 使用pg_dump备份单个表
        pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t $table -F p -v -f $table_backup
        
        # 将表备份合并到主备份文件
        Add-Content -Path $BACKUP_FILE -Value "\n-- 备份表: $table --\n"
        Get-Content -Path $table_backup | Add-Content -Path $BACKUP_FILE
        
        # 压缩单个表备份
        Compress-Archive -Path $table_backup -DestinationPath "${table_backup}.zip" -Force
        Remove-Item -Path $table_backup -Force
        
        Write-Log "表 $table 备份成功"
    }
    
    # 压缩主备份文件
    Compress-Archive -Path $BACKUP_FILE -DestinationPath "${BACKUP_FILE}.zip" -Force
    Remove-Item -Path $BACKUP_FILE -Force
    
    Write-Log "增量备份成功: ${BACKUP_FILE}.zip"
    
    # 清理3天前的增量备份
    Write-Log "开始清理3天前的增量备份文件"
    $CUTOFF_DATE = (Get-Date).AddDays(-3)
    Get-ChildItem -Path $BACKUP_DIR -Filter "*.zip" | Where-Object { $_.CreationTime -lt $CUTOFF_DATE } | Remove-Item -Force
    Write-Log "清理完成"
} catch {
    Write-Log "增量备份失败: $_"
    exit 1
} finally {
    # 清除密码环境变量
    Remove-Item env:PGPASSWORD -ErrorAction SilentlyContinue
}

Write-Log "增量备份任务完成"
exit 0