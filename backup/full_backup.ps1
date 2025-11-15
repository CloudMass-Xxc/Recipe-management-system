#!/usr/bin/env pwsh

# 数据库全量备份脚本
# 配置参数
$DB_HOST = "localhost"
$DB_PORT = "5432"
$DB_NAME = "recipe_system"
$DB_USER = "app_user"
$BACKUP_DIR = "d:/Homework/LLM/Final_assignment/Vers_4/backup/full"
$LOG_FILE = "d:/Homework/LLM/Final_assignment/Vers_4/backup/backup.log"

# 创建备份目录
if (-not (Test-Path -Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Force -Path $BACKUP_DIR | Out-Null
}

# 生成备份文件名
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_FILE = "${BACKUP_DIR}/${DB_NAME}_full_${TIMESTAMP}.sql.gz"

# 记录日志函数
function Write-Log {
    param (
        [string]$Message
    )
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $LOG_FILE -Value "[$Timestamp] $Message"
    Write-Host "[$Timestamp] $Message"
}

# 执行备份
Write-Log "开始全量备份数据库: $DB_NAME"
try {
    # 设置密码环境变量
    $env:PGPASSWORD = "app_password"
    
    # 使用pg_dump进行备份
    pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -F c -b -v -f "${BACKUP_DIR}/${DB_NAME}_full_${TIMESTAMP}.dump"
    
    # 压缩备份文件
    Compress-Archive -Path "${BACKUP_DIR}/${DB_NAME}_full_${TIMESTAMP}.dump" -DestinationPath "${BACKUP_DIR}/${DB_NAME}_full_${TIMESTAMP}.zip" -Force
    Remove-Item -Path "${BACKUP_DIR}/${DB_NAME}_full_${TIMESTAMP}.dump" -Force
    
    Write-Log "全量备份成功: ${BACKUP_DIR}/${DB_NAME}_full_${TIMESTAMP}.zip"
    
    # 清理7天前的备份文件
    Write-Log "开始清理7天前的备份文件"
    $CUTOFF_DATE = (Get-Date).AddDays(-7)
    Get-ChildItem -Path $BACKUP_DIR -Filter "*.zip" | Where-Object { $_.CreationTime -lt $CUTOFF_DATE } | Remove-Item -Force
    Write-Log "清理完成"
} catch {
    Write-Log "全量备份失败: $_"
    exit 1
} finally {
    # 清除密码环境变量
    Remove-Item env:PGPASSWORD -ErrorAction SilentlyContinue
}

Write-Log "全量备份任务完成"
exit 0