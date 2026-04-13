#!/bin/bash
# 数据库备份脚本
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
mkdir -p "$BACKUP_DIR"
cp ./asset_management.db "$BACKUP_DIR/backup_$TIMESTAMP.db"
echo "✅ 备份完成: $BACKUP_DIR/backup_$TIMESTAMP.db"
