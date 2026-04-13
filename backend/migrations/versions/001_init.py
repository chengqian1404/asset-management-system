"""初始化数据库表结构

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# 版本标识符
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """创建所有初始数据库表"""

    # 用户表
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(50), nullable=False, comment="用户名"),
        sa.Column("email", sa.String(100), nullable=False, comment="邮箱"),
        sa.Column("password_hash", sa.String(255), nullable=False, comment="密码哈希"),
        sa.Column("full_name", sa.String(100), nullable=False, comment="姓名"),
        sa.Column("department", sa.String(100), nullable=True, comment="部门"),
        sa.Column("role", sa.String(20), nullable=False, server_default="user", comment="角色"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1", comment="是否激活"),
        sa.Column("last_login", sa.DateTime(), nullable=True, comment="最后登录时间"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # 资产分类表
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(50), nullable=False, comment="分类名称"),
        sa.Column("description", sa.String(200), nullable=True, comment="分类描述"),
        sa.Column("icon", sa.String(50), nullable=True, comment="图标"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_categories_id", "categories", ["id"])

    # 资产表
    op.create_table(
        "assets",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("asset_number", sa.String(50), nullable=False, comment="资产编号"),
        sa.Column("name", sa.String(100), nullable=False, comment="资产名称"),
        sa.Column("category_id", sa.Integer(), nullable=True, comment="分类ID"),
        sa.Column("status", sa.String(20), nullable=False, server_default="idle", comment="状态"),
        sa.Column("location", sa.String(100), nullable=True, comment="位置"),
        sa.Column("owner_id", sa.Integer(), nullable=True, comment="负责人ID"),
        sa.Column("purchase_date", sa.Date(), nullable=True, comment="购买日期"),
        sa.Column("purchase_price", sa.Numeric(12, 2), nullable=True, comment="购买价格"),
        sa.Column("supplier", sa.String(100), nullable=True, comment="供应商"),
        sa.Column("description", sa.Text(), nullable=True, comment="描述"),
        sa.Column("qr_code", sa.Text(), nullable=True, comment="二维码"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="更新时间"),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_assets_id", "assets", ["id"])
    op.create_index("ix_assets_asset_number", "assets", ["asset_number"], unique=True)

    # 借用记录表
    op.create_table(
        "borrows",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False, comment="资产ID"),
        sa.Column("user_id", sa.Integer(), nullable=False, comment="申请人ID"),
        sa.Column("approver_id", sa.Integer(), nullable=True, comment="审批人ID"),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending", comment="状态"),
        sa.Column("reason", sa.Text(), nullable=True, comment="借用原因"),
        sa.Column("expected_return_date", sa.Date(), nullable=True, comment="预计归还日期"),
        sa.Column("actual_return_date", sa.Date(), nullable=True, comment="实际归还日期"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="创建时间"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="更新时间"),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["approver_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_borrows_id", "borrows", ["id"])

    # 维修记录表
    op.create_table(
        "maintenance_records",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False, comment="资产ID"),
        sa.Column("maintenance_date", sa.Date(), nullable=False, comment="维修日期"),
        sa.Column("description", sa.Text(), nullable=True, comment="描述"),
        sa.Column("cost", sa.Numeric(10, 2), nullable=True, comment="费用"),
        sa.Column("maintained_by", sa.String(100), nullable=True, comment="维修人员"),
        sa.Column("created_at", sa.Date(), nullable=False, comment="创建时间"),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_maintenance_records_id", "maintenance_records", ["id"])

    # 资产转移记录表
    op.create_table(
        "asset_transfers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False, comment="资产ID"),
        sa.Column("from_user_id", sa.Integer(), nullable=True, comment="转出人ID"),
        sa.Column("to_user_id", sa.Integer(), nullable=False, comment="转入人ID"),
        sa.Column("reason", sa.Text(), nullable=True, comment="转移原因"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="创建时间"),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"]),
        sa.ForeignKeyConstraint(["from_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["to_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_asset_transfers_id", "asset_transfers", ["id"])

    # 操作日志表
    op.create_table(
        "operation_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True, comment="用户ID"),
        sa.Column("action", sa.String(50), nullable=False, comment="操作类型"),
        sa.Column("table_name", sa.String(50), nullable=True, comment="表名"),
        sa.Column("record_id", sa.Integer(), nullable=True, comment="记录ID"),
        sa.Column("old_values", sa.Text(), nullable=True, comment="操作前数据"),
        sa.Column("new_values", sa.Text(), nullable=True, comment="操作后数据"),
        sa.Column("ip_address", sa.String(50), nullable=True, comment="IP地址"),
        sa.Column("created_at", sa.DateTime(), nullable=False, comment="创建时间"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_operation_logs_id", "operation_logs", ["id"])

    # 系统设置表
    op.create_table(
        "system_settings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("key", sa.String(100), nullable=False, comment="设置键"),
        sa.Column("value", sa.Text(), nullable=False, comment="设置值"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, comment="更新时间"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key"),
    )
    op.create_index("ix_system_settings_id", "system_settings", ["id"])


def downgrade() -> None:
    """删除所有初始化表"""
    op.drop_table("system_settings")
    op.drop_table("operation_logs")
    op.drop_table("asset_transfers")
    op.drop_table("maintenance_records")
    op.drop_table("borrows")
    op.drop_table("assets")
    op.drop_table("categories")
    op.drop_table("users")
