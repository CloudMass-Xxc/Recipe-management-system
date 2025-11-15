#!/usr/bin/env pwsh

# 数据库恢复脚本
# 参数: $1 - 备份文件路径

param (
    [string]$BackupFilePath
)

# 配置参数
$DB_HOST = "localhost"
$DB_PORT = "5432"
$DB_NAME = "recipe_system"
$DB_USER = "app_user"
$LOG_FILE = "d:/Homework/LLM/Final_assignment/Vers_4/backup/restore.log"

# 记录日志函数
function Write-Log {
    param (
        [string]$Message
    )
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $LOG_FILE -Value "[$Timestamp] $Message"
    Write-Host "[$Timestamp] $Message"
}

# 检查备份文件是否存在
if (-not (Test-Path -Path $BackupFilePath)) {
    Write-Log "错误: 备份文件不存在: $BackupFilePath"
    exit 1
}

# 执行恢复
Write-Log "开始恢复数据库: $DB_NAME"
Write-Log "使用备份文件: $BackupFilePath"
try {
    # 设置密码环境变量
    $env:PGPASSWORD = "app_password"
    
    # 检查文件类型
    if ($BackupFilePath -like "*.dump") {
        # 从自定义格式备份恢复
        pg_restore -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -v "$BackupFilePath"
        Write-Log "从自定义格式备份恢复成功"
    } elseif ($BackupFilePath -like "*.sql") {
        # 从SQL脚本恢复
        psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "$BackupFilePath"
        Write-Log "从SQL脚本恢复成功"
    } elseif ($BackupFilePath -like "*.zip") {
        # 解压ZIP文件
        $TEMP_DIR = "${BACKUP_DIR}/temp_restore_${TIMESTAMP}"
        New-Item -ItemType Directory -Force -Path $TEMP_DIR | Out-Null
        
        # 解压
        Expand-Archive -Path $BackupFilePath -DestinationPath $TEMP_DIR -Force
        
        # 查找解压后的文件
        $unzipped_file = Get-ChildItem -Path $TEMP_DIR -Recurse -File | Select-Object -First 1
        
        if ($unzipped_file -ne $null) {
            # 恢复解压后的文件
            if ($unzipped_file.Name -like "*.dump") {
                pg_restore -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -v "$($unzipped_file.FullName)"
            } elseif ($unzipped_file.Name -like "*.sql") {
                psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "$($unzipped_file.FullName)"
            }
            
            Write-Log "从ZIP文件恢复成功"
        } else {
            throw "解压后未找到备份文件"
        }
        
        # 清理临时目录
        Remove-Item -Path $TEMP_DIR -Force -Recurse
    } else {
        throw "不支持的备份文件格式"
    }
    
    Write-Log "数据库恢复成功"
} catch {
    Write-Log "数据库恢复失败: $_"
    exit 1
} finally {
    # 清除密码环境变量
    Remove-Item env:PGPASSWORD -ErrorAction SilentlyContinue
}

Write-Log "恢复任务完成"
exit 0