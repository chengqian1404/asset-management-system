# 5分钟快速开始

## 步骤一：克隆代码

```bash
git clone https://github.com/your-org/asset-management-system.git
cd asset-management-system
```

## 步骤二：启动服务

**方式A - Docker（推荐）**
```bash
docker-compose -f docker/docker-compose.yml up -d
```

**方式B - 本地启动**
```bash
bash scripts/dev.sh
```

## 步骤三：访问系统

打开浏览器访问：http://localhost:5173

## 步骤四：登录

- **用户名**：admin
- **密码**：admin123

## 步骤五：开始使用

1. 进入 **分类管理** 创建资产分类
2. 进入 **资产管理** 添加资产
3. 普通用户可以 **申请借用** 资产
4. 管理员在 **借用管理** 中审批申请

🎉 完成！
