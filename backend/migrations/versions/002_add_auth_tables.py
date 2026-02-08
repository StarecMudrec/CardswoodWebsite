"""Add auth_token and allowed_user tables

Revision ID: 002
Revises: 001
Create Date: 2026-02-08

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "auth_token",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("token", sa.String(255), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_auth_token_token"), "auth_token", ["token"], unique=True)

    op.create_table(
        "allowed_user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("allowed_user")
    op.drop_index(op.f("ix_auth_token_token"), table_name="auth_token")
    op.drop_table("auth_token")
