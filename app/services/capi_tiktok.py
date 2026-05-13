import httpx
from app.core.config import settings
from app.services.hashing import hash_sha256

async def send_tiktok_event(event_name: str, order_data: dict, phone_e164: str):
    if not settings.TIKTOK_PIXEL_CODE or not settings.TIKTOK_ACCESS_TOKEN:
        return False
        
    url = "https://business-api.tiktok.com/open_api/v1.3/pixel/track/"
    
    user_data = {
        "phone_number": hash_sha256(phone_e164)
    }
    
    if order_data.get("ttclid"):
        user_data["ttclid"] = order_data["ttclid"]
    if order_data.get("ttp"):
        user_data["ttp"] = order_data["ttp"]
        
    payload = {
        "pixel_code": settings.TIKTOK_PIXEL_CODE,
        "event": event_name,
        "event_id": order_data.get("event_id"),
        "context": {
            "ip": order_data.get("client_ip"),
            "user_agent": order_data.get("user_agent"),
            "page": {
                "url": order_data.get("source_url")
            }
        },
        "user": user_data,
        "properties": {
            "currency": order_data.get("currency", "KWD"),
            "value": float(order_data.get("total", 0))
        }
    }
    
    if settings.TIKTOK_TEST_EVENT_CODE:
        payload["test_event_code"] = settings.TIKTOK_TEST_EVENT_CODE
        
    headers = {
        "Access-Token": settings.TIKTOK_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=10.0)
            return response.status_code == 200
    except Exception:
        return False
