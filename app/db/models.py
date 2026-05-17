import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Numeric, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String, unique=True, index=True, nullable=False)
    customer_name = Column(String, nullable=False)
    phone_raw = Column(String, nullable=False)
    phone_e164 = Column(String, nullable=False)
    address = Column(Text, nullable=True)
    phone_is_test_whitelisted = Column(Boolean, default=False)

    currency = Column(String, default="KWD")
    subtotal = Column(Numeric(10, 3), nullable=False)
    total = Column(Numeric(10, 3), nullable=False)
    payment_method = Column(String, default="COD")
    status = Column(String, default="pending_confirmation") # pending_confirmation, rejected_fraud, cancelled, confirmed, delivered

    source_url = Column(String, nullable=True)
    utm_source = Column(String, nullable=True)
    utm_medium = Column(String, nullable=True)
    utm_campaign = Column(String, nullable=True)
    utm_content = Column(String, nullable=True)
    utm_term = Column(String, nullable=True)

    fbp = Column(String, nullable=True)
    fbc = Column(String, nullable=True)
    ttclid = Column(String, nullable=True)
    ttp = Column(String, nullable=True)
    sc_click_id = Column(String, nullable=True)
    sc_cookie1 = Column(String, nullable=True)

    client_ip = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    event_id = Column(String, nullable=True)

    fraud_decision = Column(String, nullable=True)
    fraud_reason = Column(String, nullable=True)
    maxmind_risk_score = Column(Numeric(5, 2), nullable=True)
    maxmind_response_json = Column(JSON, nullable=True)

    sheet_sync_status = Column(String, default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    product_id = Column(String, nullable=False)
    offer_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    quantity = Column(Numeric(10, 0), nullable=False)
    unit_price = Column(Numeric(10, 3), nullable=False)
    total_price = Column(Numeric(10, 3), nullable=False)
    is_upsell = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="items")

class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), nullable=True)
    platform = Column(String, nullable=False) # meta, tiktok, snap, sheets
    event_name = Column(String, nullable=False)
    event_id = Column(String, nullable=True)
    request_json = Column(JSON, nullable=True)
    response_json = Column(JSON, nullable=True)
    status_code = Column(Numeric(5, 0), nullable=True)
    success = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
