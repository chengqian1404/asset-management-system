#!/bin/bash
# 数据库备份脚本
# 运行方式: bash scripts/backup_db.sh（从backend目录）

DB_FILE="asset_management.db"
BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/backup_${TIMESTAMP}.db"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

if [ -f "$DB_FILE" ]; then
    cp "$DB_FILE" "$BACKUP_FILE"
    echo "✓ 数据库备份成功: $BACKUP_FILE"
else
    echo "✗ 数据库文件不存在: $DB_FILE"
    exit 1
fi
