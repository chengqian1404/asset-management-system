# 测试配置文件 - 设置测试数据库和客户端
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db
from app.models.base import Base
from app.models.user import User
from app.models.category import Category
from app.models.asset import Asset
from app.models.borrow import Borrow
from app.utils.security import hash_password
from app.constants.role import UserRole
from app.constants.status import AssetStatus
from app.constants.borrow_status import BorrowStatus

# 使用内存SQLite数据库进行测试
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # 使用StaticPool确保内存数据库跨连接共享
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """替换生产数据库会话为测试数据库会话"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# 替换依赖注入
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """每个测试函数使用独立的数据库会话"""
    # 每次测试前创建表
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # 每次测试后清空表
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """测试HTTP客户端"""
    return TestClient(app)


@pytest.fixture(scope="function")
def admin_user(db):
    """创建管理员测试用户"""
    user = User(
        username="test_admin",
        email="admin@test.com",
        password_hash=hash_password("admin123"),
        full_name="测试管理员",
        department="测试部门",
        role=UserRole.ADMIN,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def approver_user(db):
    """创建审批人测试用户"""
    user = User(
        username="test_approver",
        email="approver@test.com",
        password_hash=hash_password("approver123"),
        full_name="测试审批人",
        department="测试部门",
        role=UserRole.APPROVER,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def normal_user(db):
    """创建普通测试用户"""
    user = User(
        username="test_user",
        email="user@test.com",
        password_hash=hash_password("user123"),
        full_name="测试用户",
        department="测试部门",
        role=UserRole.USER,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def admin_token(client, admin_user):
    """获取管理员JWT令牌"""
    response = client.post("/api/auth/login", json={
        "username": "test_admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    return response.json()["data"]["token"]["access_token"]


@pytest.fixture(scope="function")
def approver_token(client, approver_user):
    """获取审批人JWT令牌"""
    response = client.post("/api/auth/login", json={
        "username": "test_approver",
        "password": "approver123"
    })
    assert response.status_code == 200
    return response.json()["data"]["token"]["access_token"]


@pytest.fixture(scope="function")
def user_token(client, normal_user):
    """获取普通用户JWT令牌"""
    response = client.post("/api/auth/login", json={
        "username": "test_user",
        "password": "user123"
    })
    assert response.status_code == 200
    return response.json()["data"]["token"]["access_token"]


@pytest.fixture(scope="function")
def test_category(db):
    """创建测试资产分类"""
    category = Category(
        name="测试设备",
        description="用于测试的设备分类",
        icon="test",
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@pytest.fixture(scope="function")
def test_asset(db, test_category, admin_user):
    """创建测试资产"""
    asset = Asset(
        asset_number="TEST-001",
        name="测试资产",
        category_id=test_category.id,
        status=AssetStatus.IDLE,
        location="测试室",
        owner_id=admin_user.id,
        description="用于测试的资产",
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@pytest.fixture(scope="function")
def test_borrow(db, test_asset, normal_user):
    """创建测试借用记录"""
    borrow = Borrow(
        asset_id=test_asset.id,
        user_id=normal_user.id,
        status=BorrowStatus.PENDING,
        reason="测试借用",
    )
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow
