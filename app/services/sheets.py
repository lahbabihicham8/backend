from datetime import datetime
from typing import Any

import httpx

from app.core.config import settings
from app.services.catalog import CATALOG


DEFAULT_SKU = "KH-PROD"


def _sku_for(product_id: str) -> str:
    product = CATALOG.get(product_id) or {}
    return product.get("sku") or DEFAULT_SKU


def _arabic_name_for(item: dict) -> str:
    product = CATALOG.get(item.get("product_id")) or {}
    if product.get("title"):
        return product["title"]
    # Fall back to the title that was stored on the order item (already Arabic
    # for catalog products, may contain "(Upsell)" suffix for upsell line items).
    return item.get("title") or item.get("product_id") or ""


def _format_phone(order: dict) -> str:
    e164 = (order.get("phone_e164") or "").lstrip("+")
    if e164:
        return e164
    raw = "".join(c for c in (order.get("phone_raw") or "") if c.isdigit())
    if not raw:
        return ""
    if raw.startswith("965"):
        return raw
    return f"965{raw}"


def _format_date(order: dict) -> str:
    created_at = order.get("created_at")
    if isinstance(created_at, datetime):
        return created_at.strftime("%d/%m/%Y")
    if isinstance(created_at, str) and created_at:
        try:
            return datetime.fromisoformat(created_at.replace("Z", "+00:00")).strftime("%d/%m/%Y")
        except ValueError:
            pass
    return datetime.utcnow().strftime("%d/%m/%Y")


def _format_total(value: Any) -> str:
    if value in (None, ""):
        return ""
    return str(value)


def build_sheet_row(order_data: dict) -> dict:
    items = order_data.get("items") or []
    products_ar = [_arabic_name_for(item) for item in items]
    skus = [_sku_for(item.get("product_id")) for item in items]
    quantities = [str(int(item.get("quantity") or 0)) for item in items]

    return {
        "date": _format_date(order_data),
        "order_id": order_data.get("order_number") or order_data.get("order_id") or "",
        "country": "Kuwait",
        "name": order_data.get("customer_name") or "",
        "phone": _format_phone(order_data),
        "product": "/".join(products_ar),
        "sku": "/".join(skus),
        "quantity": "/".join(quantities),
        "total_price": _format_total(order_data.get("total")),
        "currency": "KWD",
        "status": ""
    }


async def send_to_sheets(order_data: dict) -> bool:
    if not settings.ORDER_WEBHOOK_URL:
        return False

    row = build_sheet_row(order_data)
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.post(
                settings.ORDER_WEBHOOK_URL,
                json=row,
                timeout=10.0,
            )
            return 200 <= response.status_code < 300
    except Exception:
        return False
