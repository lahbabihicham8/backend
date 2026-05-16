from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from sqlalchemy.orm import Session
from decimal import Decimal
import uuid
from datetime import datetime

from app.db.session import get_db
from app.db.models import Order, OrderItem
from app.schemas.orders import OrderCreate, OrderResponse, UpsellResponse, PublicOrderResponse
from app.services.phone import normalize_kuwait_phone
from app.services.catalog import get_offer_details
from app.services.maxmind import inspect_order
from app.services.sheets import send_to_sheets
from app.services.capi_meta import send_meta_event
from app.services.capi_tiktok import send_tiktok_event
from app.services.capi_snap import send_snap_event
from app.core.config import settings

router = APIRouter()

def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host

@router.post("", response_model=OrderResponse)
async def create_order(
    order_in: OrderCreate, 
    request: Request, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # 1. Validate Phone
    phone_res = normalize_kuwait_phone(order_in.phone)
    if not phone_res.valid:
        raise HTTPException(status_code=400, detail=phone_res.error)
        
    is_test_phone = phone_res.local_number in settings.test_phones_list

    # 2. Calculate Totals
    subtotal = Decimal("0.000")
    validated_items = []
    
    for item in order_in.items:
        offer_details = get_offer_details(item.product_id, item.offer_id)
        if not offer_details:
            raise HTTPException(status_code=400, detail="PRODUCT_UNAVAILABLE")
            
        validated_items.append({
            "product_id": item.product_id,
            "offer_id": item.offer_id,
            "title": offer_details["product_title"],
            "quantity": offer_details["quantity"],
            "unit_price": offer_details["unit_price"],
            "total_price": offer_details["total_price"]
        })
        subtotal += offer_details["total_price"]

    total = subtotal # No shipping fee for now
    
    # 3. Fraud Check
    client_ip = get_client_ip(request)
    user_agent = request.headers.get("User-Agent", "")
    
    order_number = f"KH-{datetime.utcnow().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"
    
    fraud_decision = None
    fraud_reason = None
    maxmind_risk_score = None
    maxmind_response = None
    
    if is_test_phone:
        fraud_decision = True
        fraud_reason = "TEST_PHONE_WHITELIST"
    else:
        fraud_res = inspect_order(
            ip=client_ip,
            user_agent=user_agent,
            order_data={
                "order_number": order_number,
                "customer_name": order_in.customer_name,
                "total": float(total)
            }
        )
        fraud_decision = fraud_res.allowed
        fraud_reason = fraud_res.reason
        maxmind_risk_score = fraud_res.risk_score
        maxmind_response = fraud_res.response_json
        
        if not fraud_decision:
            # We could save the rejected order to DB here if we want to track them
            raise HTTPException(status_code=400, detail=fraud_reason)

    # 4. Save Order
    db_order = Order(
        order_number=order_number,
        customer_name=order_in.customer_name,
        phone_raw=order_in.phone,
        phone_e164=phone_res.e164,
        address=order_in.address,
        phone_is_test_whitelisted=is_test_phone,
        currency=order_in.currency,
        subtotal=subtotal,
        total=total,
        payment_method=order_in.payment_method,
        status="pending_confirmation",
        source_url=order_in.landing_page_url,
        utm_source=order_in.utm_source,
        utm_medium=order_in.utm_medium,
        utm_campaign=order_in.utm_campaign,
        utm_content=order_in.utm_content,
        utm_term=order_in.utm_term,
        fbp=order_in.fbp,
        fbc=order_in.fbc,
        ttclid=order_in.ttclid,
        ttp=order_in.ttp,
        sc_click_id=order_in.sc_click_id,
        sc_cookie1=order_in.sc_cookie1,
        client_ip=client_ip,
        user_agent=user_agent,
        event_id=order_in.event_id,
        fraud_decision=str(fraud_decision),
        fraud_reason=fraud_reason,
        maxmind_risk_score=maxmind_risk_score,
        maxmind_response_json=maxmind_response
    )
    
    db.add(db_order)
    db.flush() # Get ID
    
    for item in validated_items:
        db_item = OrderItem(
            order_id=db_order.id,
            **item
        )
        db.add(db_item)
        
    db.commit()
    db.refresh(db_order)
    
    # 5. Background Tasks (Webhooks, CAPI)
    order_dict = {
        "order_id": str(db_order.id),
        "order_number": db_order.order_number,
        "customer_name": db_order.customer_name,
        "phone_raw": db_order.phone_raw,
        "status": db_order.status,
        "currency": db_order.currency,
        "subtotal": str(db_order.subtotal),
        "total": str(db_order.total),
        "payment_method": db_order.payment_method,
        "client_ip": db_order.client_ip,
        "country": "KW",
        "user_agent": db_order.user_agent,
        "event_id": db_order.event_id,
        "source_url": db_order.source_url,
        "fbp": db_order.fbp,
        "fbc": db_order.fbc,
        "ttclid": db_order.ttclid,
        "ttp": db_order.ttp,
        "sc_cookie1": db_order.sc_cookie1,
        "items": [
            {
                "product_id": i.product_id,
                "offer_id": i.offer_id,
                "title": i.title,
                "quantity": int(i.quantity),
                "unit_price": str(i.unit_price),
                "total_price": str(i.total_price),
                "is_upsell": i.is_upsell
            } for i in db_order.items
        ]
    }
    
    background_tasks.add_task(send_to_sheets, order_dict)
    background_tasks.add_task(send_meta_event, "Purchase", order_dict, db_order.phone_e164)
    background_tasks.add_task(send_tiktok_event, "CompletePayment", order_dict, db_order.phone_e164)
    background_tasks.add_task(send_snap_event, "PURCHASE", order_dict, db_order.phone_e164)
    
    return OrderResponse(
        order_id=str(db_order.id),
        order_number=db_order.order_number,
        status=db_order.status,
        currency=db_order.currency,
        total=float(db_order.total),
        event_id=db_order.event_id,
        upsell_expires_in_seconds=15
    )

@router.post("/{order_id}/upsell", response_model=UpsellResponse)
async def accept_upsell(
    order_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    # Check if already has upsell
    has_upsell = any(item.is_upsell for item in db_order.items)
    if has_upsell:
        raise HTTPException(status_code=400, detail="UPSELL_ALREADY_ACCEPTED")
        
    # Add upsell item
    offer_details = get_offer_details("khafeefa-waist-fan-powerbank", "post_order_upsell")
    if not offer_details:
        raise HTTPException(status_code=400, detail="PRODUCT_UNAVAILABLE")
        
    db_item = OrderItem(
        order_id=db_order.id,
        product_id="khafeefa-waist-fan-powerbank",
        offer_id="post_order_upsell",
        title=offer_details["product_title"] + " (Upsell)",
        quantity=offer_details["quantity"],
        unit_price=offer_details["unit_price"],
        total_price=offer_details["total_price"],
        is_upsell=True
    )
    
    db_order.subtotal += offer_details["total_price"]
    db_order.total += offer_details["total_price"]
    
    db.add(db_item)
    db.commit()
    db.refresh(db_order)
    
    # Background Tasks
    order_dict = {
        "order_id": str(db_order.id),
        "order_number": db_order.order_number,
        "customer_name": db_order.customer_name,
        "phone_raw": db_order.phone_raw,
        "status": db_order.status,
        "currency": db_order.currency,
        "subtotal": str(db_order.subtotal),
        "total": str(db_order.total),
        "payment_method": db_order.payment_method,
        "items": [
            {
                "product_id": i.product_id,
                "offer_id": i.offer_id,
                "title": i.title,
                "quantity": int(i.quantity),
                "unit_price": str(i.unit_price),
                "total_price": str(i.total_price),
                "is_upsell": i.is_upsell
            } for i in db_order.items
        ]
    }
    
    background_tasks.add_task(send_to_sheets, order_dict)
    # Could send additional CAPI event here if needed
    
    return UpsellResponse(
        order_id=str(db_order.id),
        order_number=db_order.order_number,
        status=db_order.status,
        currency=db_order.currency,
        total=float(db_order.total),
        message="Upsell added successfully"
    )

@router.get("/{order_id}", response_model=PublicOrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    return PublicOrderResponse(
        order_id=str(db_order.id),
        order_number=db_order.order_number,
        customer_name=db_order.customer_name,
        status=db_order.status,
        currency=db_order.currency,
        total=float(db_order.total)
    )
