# Python包安装配置
from setuptools import setup, find_packages

setup(
    name="asset-management-backend",
    version="1.0.0",
    description="资产管理系统后端API",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastapi==0.109.0",
        "uvicorn[standard]==0.27.0",
        "sqlalchemy==2.0.25",
        "alembic==1.13.1",
        "pydantic==2.5.3",
        "pydantic-settings==2.1.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6",
    ],
)
