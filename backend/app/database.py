# 数据库连接配置模块
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings


# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite需要此参数
    echo=settings.DEBUG,                         # 调试模式下输出SQL语句
)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """启用SQLite外键约束"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """获取数据库会话的依赖函数，用于FastAPI依赖注入"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """创建所有数据库表"""
    from app.models.base import Base
    # 导入所有模型以确保表被创建
    from app.models import user, asset, category, borrow, maintenance, asset_transfer, operation_log
    Base.metadata.create_all(bind=engine)
