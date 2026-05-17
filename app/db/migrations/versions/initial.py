"""empty message

Revision ID: initial
Revises: 
Create Date: 2026-05-13 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('orders',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('order_number', sa.String(), nullable=False),
        sa.Column('customer_name', sa.String(), nullable=False),
        sa.Column('phone_raw', sa.String(), nullable=False),
        sa.Column('phone_e164', sa.String(), nullable=False),
        sa.Column('phone_is_test_whitelisted', sa.Boolean(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('subtotal', sa.Numeric(precision=10, scale=3), nullable=False),
        sa.Column('total', sa.Numeric(precision=10, scale=3), nullable=False),
        sa.Column('payment_method', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('source_url', sa.String(), nullable=True),
        sa.Column('utm_source', sa.String(), nullable=True),
        sa.Column('utm_medium', sa.String(), nullable=True),
        sa.Column('utm_campaign', sa.String(), nullable=True),
        sa.Column('utm_content', sa.String(), nullable=True),
        sa.Column('utm_term', sa.String(), nullable=True),
        sa.Column('fbp', sa.String(), nullable=True),
        sa.Column('fbc', sa.String(), nullable=True),
        sa.Column('ttclid', sa.String(), nullable=True),
        sa.Column('ttp', sa.String(), nullable=True),
        sa.Column('sc_click_id', sa.String(), nullable=True),
        sa.Column('sc_cookie1', sa.String(), nullable=True),
        sa.Column('client_ip', sa.String(), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('event_id', sa.String(), nullable=True),
        sa.Column('fraud_decision', sa.String(), nullable=True),
        sa.Column('fraud_reason', sa.String(), nullable=True),
        sa.Column('maxmind_risk_score', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('maxmind_response_json', sa.JSON(), nullable=True),
        sa.Column('sheet_sync_status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_order_number'), 'orders', ['order_number'], unique=True)
    
    op.create_table('order_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('order_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', sa.String(), nullable=False),
        sa.Column('offer_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=10, scale=0), nullable=False),
        sa.Column('unit_price', sa.Numeric(precision=10, scale=3), nullable=False),
        sa.Column('total_price', sa.Numeric(precision=10, scale=3), nullable=False),
        sa.Column('is_upsell', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('event_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('order_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('platform', sa.String(), nullable=False),
        sa.Column('event_name', sa.String(), nullable=False),
        sa.Column('event_id', sa.String(), nullable=True),
        sa.Column('request_json', sa.JSON(), nullable=True),
        sa.Column('response_json', sa.JSON(), nullable=True),
        sa.Column('status_code', sa.Numeric(precision=5, scale=0), nullable=True),
        sa.Column('success', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('event_logs')
    op.drop_table('order_items')
    op.drop_index(op.f('ix_orders_order_number'), table_name='orders')
    op.drop_table('orders')
