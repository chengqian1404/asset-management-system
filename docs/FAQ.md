# 常见问题

## Q: 如何重置管理员密码？

```bash
cd backend
python scripts/create_admin.py
```

## Q: 如何备份数据？

```bash
bash backend/scripts/backup_db.sh
```

## Q: 支持哪些数据库？

- **SQLite**：默认，适合单机/开发环境
- **PostgreSQL**：适合生产环境，修改 `DATABASE_URL` 即可

## Q: 如何修改端口？

- **后端**：`uvicorn app.main:app --port 8001`
- **前端**：修改 `frontend/vite.config.js` 中的 `server.port`

## Q: 资产编号格式是什么？

推荐格式：`类别简称-年份-序号`，例如：`IT-2024-001`

## Q: 如何批量导入资产？

1. 下载Excel模板（功能开发中）
2. 按模板填写资产数据
3. 在资产列表页面点击"批量导入"

## Q: JWT Token有效期是多久？

- **访问Token**：30分钟（可在 `.env` 中修改）
- **刷新Token**：7天
