#!/bin/bash
# 数据库恢复脚本
if [ -z "$1" ]; then
    echo "用法: ./restore_db.sh <备份文件路径>"
    exit 1
fi
cp "$1" ./asset_management.db
echo "✅ 恢复完成"
