import httpx
import time
from app.core.config import settings
from app.services.hashing import hash_sha256

async def send_snap_event(event_name: str, order_data: dict, phone_e164: str):
    if not settings.SNAP_PIXEL_ID or not settings.SNAP_ACCESS_TOKEN:
        return False
        
    url = "https://tr.snapchat.com/v2/conversion"
    
    event = {
        "pixel_id": settings.SNAP_PIXEL_ID,
        "event_type": event_name,
        "event_conversion_type": "WEB",
        "timestamp": str(int(time.time())),
        "client_dedup_id": order_data.get("event_id"),
        "hashed_phone_number": hash_sha256(phone_e164),
        "client_ip_address": order_data.get("client_ip"),
        "user_agent": order_data.get("user_agent"),
        "page_url": order_data.get("source_url"),
        "currency": order_data.get("currency", "KWD"),
        "price": float(order_data.get("total", 0))
    }
    
    if order_data.get("sc_cookie1"):
        event["uuid_c1"] = order_data["sc_cookie1"]
        
    headers = {
        "Authorization": f"Bearer {settings.SNAP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=event, headers=headers, timeout=10.0)
            return response.status_code == 200
    except Exception:
        return False
