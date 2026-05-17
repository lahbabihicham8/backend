import httpx
from app.core.config import settings

async def send_to_sheets(order_data: dict):
    if not settings.ORDER_WEBHOOK_URL:
        return False

    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "secret": settings.ORDER_WEBHOOK_SECRET,
                "order": order_data
            }
            response = await client.post(settings.ORDER_WEBHOOK_URL, json=payload, timeout=10.0)
            return response.status_code == 200
    except Exception:
        return False
