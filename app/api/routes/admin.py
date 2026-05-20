from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings
from app.services import sheets

router = APIRouter()


class WebhookProbeIn(BaseModel):
    order_id: Optional[str] = None
    name: Optional[str] = "Webhook Probe"
    phone: Optional[str] = "96550000000"


def _mask_url(url: str) -> str:
    if not url:
        return ""
    if len(url) <= 40:
        return url[:6] + "...." + url[-4:]
    return url[:32] + "...." + url[-12:]


@router.get("/webhook-status")
def webhook_status():
    """Show whether the sheets webhook is configured and the last attempt."""
    return {
        "configured": bool(settings.ORDER_WEBHOOK_URL),
        "url_preview": _mask_url(settings.ORDER_WEBHOOK_URL),
        "last_attempt": sheets.last_webhook_attempt,
    }


@router.post("/webhook-test")
async def webhook_test(probe: WebhookProbeIn = WebhookProbeIn()):
    """Send a synthetic row to the configured webhook and return the result."""
    row = {
        "date": datetime.utcnow().strftime("%d/%m/%Y"),
        "order_id": probe.order_id or f"KH-PROBE-{datetime.utcnow().strftime('%H%M%S')}",
        "country": "Kuwait",
        "name": probe.name or "Webhook Probe",
        "phone": probe.phone or "96550000000",
        "product": "مروحة خفيفة للخصر مع باور بانك",
        "sku": "KH-WF-PB-001",
        "quantity": "1",
        "total_price": "12.900",
        "currency": "KWD",
        "status": "",
    }
    result = await sheets.post_row_to_webhook(row)
    return result
