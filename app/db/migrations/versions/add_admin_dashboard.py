"""add admin dashboard tables and columns

Adds the `clicks` table used for conversion-rate analytics, and the
session_id / country_code / is_vpn / is_valid_traffic / admin_notes
columns on `orders`.

Revision ID: add_admin_dashboard
Revises: add_order_address
Create Date: 2026-05-24 04:55:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "add_admin_dashboard"
down_revision = "add_order_address"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- orders: new analytic / admin columns ---
    op.add_column("orders", sa.Column("session_id", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("country_code", sa.String(length=2), nullable=True))
    op.add_column(
        "orders",
        sa.Column("is_vpn", sa.Boolean(), nullable=True, server_default=sa.false()),
    )
    op.add_column(
        "orders",
        sa.Column(
            "is_valid_traffic",
            sa.Boolean(),
            nullable=True,
            server_default=sa.true(),
        ),
    )
    op.add_column("orders", sa.Column("admin_notes", sa.Text(), nullable=True))
    op.create_index("ix_orders_session_id", "orders", ["session_id"])
    op.create_index("ix_orders_country_code", "orders", ["country_code"])
    op.create_index("ix_orders_is_valid_traffic", "orders", ["is_valid_traffic"])
    op.create_index("ix_orders_created_at", "orders", ["created_at"])
    op.create_index(
        "ix_orders_created_at_valid", "orders", ["created_at", "is_valid_traffic"]
    )

    # --- clicks ---
    op.create_table(
        "clicks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("session_id", sa.String(), nullable=False),
        sa.Column("visitor_id", sa.String(), nullable=True),
        sa.Column("client_ip", sa.String(), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("referrer", sa.Text(), nullable=True),
        sa.Column("landing_page_url", sa.Text(), nullable=True),
        sa.Column("page_path", sa.String(), nullable=True),
        sa.Column("country_code", sa.String(length=2), nullable=True),
        sa.Column(
            "is_vpn",
            sa.Boolean(),
            nullable=True,
            server_default=sa.false(),
        ),
        sa.Column(
            "is_valid_traffic",
            sa.Boolean(),
            nullable=True,
            server_default=sa.true(),
        ),
        sa.Column("maxmind_risk_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("utm_source", sa.String(), nullable=True),
        sa.Column("utm_medium", sa.String(), nullable=True),
        sa.Column("utm_campaign", sa.String(), nullable=True),
        sa.Column("utm_content", sa.String(), nullable=True),
        sa.Column("utm_term", sa.String(), nullable=True),
        sa.Column("fbp", sa.String(), nullable=True),
        sa.Column("fbc", sa.String(), nullable=True),
        sa.Column("ttclid", sa.String(), nullable=True),
        sa.Column("sc_click_id", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_clicks_session_id", "clicks", ["session_id"])
    op.create_index("ix_clicks_visitor_id", "clicks", ["visitor_id"])
    op.create_index("ix_clicks_country_code", "clicks", ["country_code"])
    op.create_index("ix_clicks_is_vpn", "clicks", ["is_vpn"])
    op.create_index("ix_clicks_is_valid_traffic", "clicks", ["is_valid_traffic"])
    op.create_index("ix_clicks_utm_source", "clicks", ["utm_source"])
    op.create_index("ix_clicks_utm_campaign", "clicks", ["utm_campaign"])
    op.create_index("ix_clicks_created_at", "clicks", ["created_at"])
    op.create_index(
        "ix_clicks_created_at_valid", "clicks", ["created_at", "is_valid_traffic"]
    )


def downgrade() -> None:
    op.drop_index("ix_clicks_created_at_valid", table_name="clicks")
    op.drop_index("ix_clicks_created_at", table_name="clicks")
    op.drop_index("ix_clicks_utm_campaign", table_name="clicks")
    op.drop_index("ix_clicks_utm_source", table_name="clicks")
    op.drop_index("ix_clicks_is_valid_traffic", table_name="clicks")
    op.drop_index("ix_clicks_is_vpn", table_name="clicks")
    op.drop_index("ix_clicks_country_code", table_name="clicks")
    op.drop_index("ix_clicks_visitor_id", table_name="clicks")
    op.drop_index("ix_clicks_session_id", table_name="clicks")
    op.drop_table("clicks")

    op.drop_index("ix_orders_created_at_valid", table_name="orders")
    op.drop_index("ix_orders_created_at", table_name="orders")
    op.drop_index("ix_orders_is_valid_traffic", table_name="orders")
    op.drop_index("ix_orders_country_code", table_name="orders")
    op.drop_index("ix_orders_session_id", table_name="orders")
    op.drop_column("orders", "admin_notes")
    op.drop_column("orders", "is_valid_traffic")
    op.drop_column("orders", "is_vpn")
    op.drop_column("orders", "country_code")
    op.drop_column("orders", "session_id")
