from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from decimal import Decimal

class OrderItemCreate(BaseModel):
    product_id: str
    offer_id: str
    quantity: int

class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=80)
    phone: str
    address: Optional[str] = None
    items: List[OrderItemCreate]
    currency: str = "KWD"
    payment_method: str = "COD"
    event_id: str
    landing_page_url: Optional[str] = None
    session_id: Optional[str] = None

    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None

    fbp: Optional[str] = None
    fbc: Optional[str] = None
    ttclid: Optional[str] = None
    ttp: Optional[str] = None
    sc_click_id: Optional[str] = None
    sc_cookie1: Optional[str] = None

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str) -> str:
        if value.upper() != "KWD":
            raise ValueError("UNSUPPORTED_CURRENCY")
        return "KWD"

class OrderResponse(BaseModel):
    order_id: str
    order_number: str
    status: str
    currency: str
    total: float
    event_id: str
    upsell_expires_in_seconds: int = 15

class UpsellResponse(BaseModel):
    order_id: str
    order_number: str
    status: str
    currency: str
    total: float
    message: str

class PublicOrderResponse(BaseModel):
    order_id: str
    order_number: str
    customer_name: str
    status: str
    currency: str
    total: float
