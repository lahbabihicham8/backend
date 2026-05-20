from datetime import datetime
from typing import Optional

import httpx
from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings
from app.services import sheets

router = APIRouter()


class WebhookProbeIn(BaseModel):
    order_id: Optional[str] = None
    name: Optional[str] = "Webhook Probe"
    phone: Optional[str] = "96550000000"
    # Optional override; if provided we POST to this URL instead of the one
    # in ORDER_WEBHOOK_URL. Lets us validate an Apps Script deployment even
    # before EasyPanel env vars are set.
    webhook_url: Optional[str] = None


def _mask_url(url: str) -> str:
    if not url:
        return ""
    if len(url) <= 40:
        return url[:6] + "...." + url[-4:]
    return url[:32] + "...." + url[-12:]


def _make_probe_row(probe: WebhookProbeIn) -> dict:
    return {
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
    row = _make_probe_row(probe)

    if probe.webhook_url:
        # Direct probe to an ad-hoc URL (e.g. while debugging the Apps Script).
        result = {
            "ok": False,
            "url_configured": True,
            "url_used": _mask_url(probe.webhook_url),
            "status_code": None,
            "response_body": None,
            "error": None,
            "row": row,
        }
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.post(probe.webhook_url, json=row, timeout=15.0)
                result["status_code"] = response.status_code
                result["response_body"] = response.text[:1000]
                result["ok"] = 200 <= response.status_code < 300
        except Exception as exc:
            result["error"] = f"{type(exc).__name__}: {exc}"
        return result

    return await sheets.post_row_to_webhook(row)
