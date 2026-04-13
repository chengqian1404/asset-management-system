#!/bin/bash
# 数据库恢复脚本
# 运行方式: bash scripts/restore_db.sh <备份文件名>（从backend目录）

BACKUP_DIR="backups"
DB_FILE="asset_management.db"

if [ -z "$1" ]; then
    echo "用法: bash scripts/restore_db.sh <备份文件名>"
    echo "可用的备份文件:"
    ls -la "$BACKUP_DIR"/*.db 2>/dev/null || echo "  无备份文件"
    exit 1
fi

BACKUP_FILE="${BACKUP_DIR}/$1"

if [ -f "$BACKUP_FILE" ]; then
    # 先备份当前数据库
    if [ -f "$DB_FILE" ]; then
        cp "$DB_FILE" "${DB_FILE}.bak"
        echo "✓ 当前数据库已备份为: ${DB_FILE}.bak"
    fi

    cp "$BACKUP_FILE" "$DB_FILE"
    echo "✓ 数据库恢复成功: $BACKUP_FILE -> $DB_FILE"
else
    echo "✗ 备份文件不存在: $BACKUP_FILE"
    exit 1
fi
