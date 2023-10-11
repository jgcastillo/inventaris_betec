"""create users and roles tables

Revision ID: 76042329dfd1
Revises: 3b40e6e7a0a8
Create Date: 2023-06-20 11:09:33.263976

"""
from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = "76042329dfd1"
down_revision = "3b40e6e7a0a8"
branch_labels = None
depends_on = None


def create_roles_table():
    op.create_table(
        "roles",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("role", sa.Text, unique=True, index=True),
        sa.Column("permissions", sa.ARRAY(sa.String)),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_by", UUID, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_by", UUID, nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )


def create_users_table():
    op.create_table(
        "users",
        sa.Column("id", UUID, primary_key=True, default=uuid4()),
        sa.Column("username", sa.String(40), unique=True, index=True, nullable=False),
        sa.Column("fullname", sa.Text, nullable=False),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column("email", sa.String(60), unique=True, index=True, nullable=False),
        sa.Column("is_superadmin", sa.Boolean, nullable=True, default=False),
        sa.Column("role_id", UUID, sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_by", UUID, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_by", UUID, nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )


def upgrade() -> None:
    create_roles_table()
    create_users_table()


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("roles")
