#!/bin/bash

# 备份脚本 - backup_db.sh
BACKUP_DIR="d:/Homework/LLM/Final_assignment/Vers_4/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/recipe_system_backup_${TIMESTAMP}.sql.gz"

# 创建备份目录
mkdir -p "${BACKUP_DIR}"

# 执行备份
pg_dump -U app_user -d recipe_system | gzip > "${BACKUP_FILE}"

echo "备份完成: ${BACKUP_FILE}"

# 保留最近30天的备份
find "${BACKUP_DIR}" -name "recipe_system_backup_*.sql.gz" -mtime +30 -delete