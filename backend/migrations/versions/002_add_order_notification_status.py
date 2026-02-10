"""Add order notification_status and notification_error

Revision ID: 002
Revises: 001
Create Date: 2026-02-08

"""
from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("orders", sa.Column("notification_status", sa.String(20), nullable=True))
    op.add_column("orders", sa.Column("notification_error", sa.String(512), nullable=True))


def downgrade():
    op.drop_column("orders", "notification_error")
    op.drop_column("orders", "notification_status")
