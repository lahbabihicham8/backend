"""add order address

Revision ID: add_order_address
Revises: initial
Create Date: 2026-05-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "add_order_address"
down_revision = "initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("orders", sa.Column("address", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("orders", "address")
