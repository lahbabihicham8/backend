import httpx
import time
from app.core.config import settings
from app.services.hashing import hash_sha256

async def send_meta_event(event_name: str, order_data: dict, phone_e164: str):
    if not settings.META_PIXEL_ID or not settings.META_ACCESS_TOKEN:
        return False

    url = f"https://graph.facebook.com/v19.0/{settings.META_PIXEL_ID}/events"

    user_data = {
        "ph": hash_sha256(phone_e164),
        "client_ip_address": order_data.get("client_ip"),
        "client_user_agent": order_data.get("user_agent"),
    }

    if order_data.get("fbp"):
        user_data["fbp"] = order_data["fbp"]
    if order_data.get("fbc"):
        user_data["fbc"] = order_data["fbc"]

    event = {
        "event_name": event_name,
        "event_time": int(time.time()),
        "action_source": "website",
        "event_id": order_data.get("event_id"),
        "event_source_url": order_data.get("source_url"),
        "user_data": user_data,
        "custom_data": {
            "currency": order_data.get("currency", "KWD"),
            "value": float(order_data.get("total", 0))
        }
    }

    payload = {
        "data": [event],
        "access_token": settings.META_ACCESS_TOKEN
    }

    if settings.META_TEST_EVENT_CODE:
        payload["test_event_code"] = settings.META_TEST_EVENT_CODE

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            return response.status_code == 200
    except Exception:
        return False
