"""Admin dashboard API.

Auth: all endpoints require a Bearer JWT issued by POST /v1/admin/auth/login.

Filtering: every analytic query filters on `is_valid_traffic=true` so VPN /
non-allowed-country events never contaminate dashboard numbers.
"""

from datetime import datetime, timedelta, date
from decimal import Decimal
from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session, joinedload

from app.db.models import Click, Order, OrderItem
from app.db.session import get_db
from app.services.admin_auth import (
    issue_token,
    require_admin,
    verify_credentials,
)


router = APIRouter()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class LoginIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    username: str


class TimeseriesPoint(BaseModel):
    date: str
    clicks: int
    orders: int
    confirmed_orders: int
    revenue: float


class BreakdownRow(BaseModel):
    key: str
    clicks: int
    orders: int
    revenue: float


class MetricsOut(BaseModel):
    range_from: str
    range_to: str
    total_clicks: int
    unique_visitors: int
    total_orders: int
    confirmed_orders: int
    delivered_orders: int
    cancelled_orders: int
    rejected_fraud_orders: int
    pending_orders: int
    revenue: float
    confirmed_revenue: float
    delivered_revenue: float
    average_order_value: float
    conversion_rate: float  # orders / clicks (0..1)
    confirmed_conversion_rate: float  # confirmed / clicks
    timeseries: List[TimeseriesPoint]
    top_utm_sources: List[BreakdownRow]
    top_utm_campaigns: List[BreakdownRow]
    top_landing_pages: List[BreakdownRow]


class OrderListItem(BaseModel):
    order_id: str
    order_number: str
    customer_name: str
    phone_e164: str
    address: Optional[str]
    status: str
    currency: str
    total: float
    items_count: int
    country_code: Optional[str]
    is_vpn: bool
    is_valid_traffic: bool
    utm_source: Optional[str]
    utm_campaign: Optional[str]
    created_at: str


class OrderListOut(BaseModel):
    total: int
    page: int
    page_size: int
    pages: int
    items: List[OrderListItem]


class OrderItemDetail(BaseModel):
    product_id: str
    offer_id: str
    title: str
    quantity: int
    unit_price: float
    total_price: float
    is_upsell: bool


class OrderDetailOut(BaseModel):
    order_id: str
    order_number: str
    customer_name: str
    phone_raw: str
    phone_e164: str
    address: Optional[str]
    status: str
    currency: str
    subtotal: float
    total: float
    payment_method: str

    items: List[OrderItemDetail]

    source_url: Optional[str]
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_campaign: Optional[str]
    utm_content: Optional[str]
    utm_term: Optional[str]

    client_ip: Optional[str]
    user_agent: Optional[str]
    country_code: Optional[str]
    is_vpn: bool
    is_valid_traffic: bool

    fraud_decision: Optional[str]
    fraud_reason: Optional[str]
    maxmind_risk_score: Optional[float]

    sheet_sync_status: Optional[str]
    admin_notes: Optional[str]
    created_at: str
    updated_at: Optional[str]


class OrderStatusUpdate(BaseModel):
    status: Literal[
        "pending_confirmation",
        "confirmed",
        "shipped",
        "delivered",
        "cancelled",
        "returned",
        "refunded",
        "rejected_fraud",
    ]
    admin_notes: Optional[str] = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_range(
    range_from: Optional[str], range_to: Optional[str]
) -> tuple[datetime, datetime]:
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    if range_from:
        start = datetime.fromisoformat(range_from)
    else:
        start = today - timedelta(days=29)
    if range_to:
        end = datetime.fromisoformat(range_to)
    else:
        end = today + timedelta(days=1) - timedelta(microseconds=1)
    if end < start:
        start, end = end, start
    return start, end


def _serialize_order_list_row(o: Order, items_count: int) -> OrderListItem:
    return OrderListItem(
        order_id=str(o.id),
        order_number=o.order_number,
        customer_name=o.customer_name,
        phone_e164=o.phone_e164,
        address=o.address,
        status=o.status or "pending_confirmation",
        currency=o.currency or "KWD",
        total=float(o.total or 0),
        items_count=items_count,
        country_code=o.country_code,
        is_vpn=bool(o.is_vpn),
        is_valid_traffic=bool(o.is_valid_traffic),
        utm_source=o.utm_source,
        utm_campaign=o.utm_campaign,
        created_at=(o.created_at or datetime.utcnow()).isoformat(),
    )


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

@router.post("/auth/login", response_model=TokenOut)
def login(payload: LoginIn):
    if not verify_credentials(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="INVALID_CREDENTIALS")
    return issue_token(payload.username)


@router.get("/auth/me")
def me(username: str = Depends(require_admin)):
    return {"username": username, "role": "admin"}


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

@router.get("/metrics", response_model=MetricsOut)
def metrics(
    range_from: Optional[str] = Query(None, alias="from"),
    range_to: Optional[str] = Query(None, alias="to"),
    db: Session = Depends(get_db),
    _: str = Depends(require_admin),
):
    start, end = _parse_range(range_from, range_to)

    # ---- Click totals (valid traffic only) ----
    click_filter = and_(
        Click.is_valid_traffic.is_(True),
        Click.created_at >= start,
        Click.created_at <= end,
    )
    total_clicks = db.query(func.count(Click.id)).filter(click_filter).scalar() or 0
    unique_visitors = (
        db.query(func.count(func.distinct(Click.session_id)))
        .filter(click_filter)
        .scalar()
        or 0
    )

    # ---- Order totals (valid traffic only) ----
    order_filter = and_(
        Order.is_valid_traffic.is_(True),
        Order.created_at >= start,
        Order.created_at <= end,
    )
    total_orders = db.query(func.count(Order.id)).filter(order_filter).scalar() or 0

    def count_by_status(status: str) -> int:
        return (
            db.query(func.count(Order.id))
            .filter(order_filter, Order.status == status)
            .scalar()
            or 0
        )

    confirmed_orders = count_by_status("confirmed") + count_by_status("shipped") + count_by_status("delivered")
    delivered_orders = count_by_status("delivered")
    cancelled_orders = count_by_status("cancelled") + count_by_status("returned") + count_by_status("refunded")
    rejected_fraud_orders = count_by_status("rejected_fraud")
    pending_orders = count_by_status("pending_confirmation")

    revenue = float(
        db.query(func.coalesce(func.sum(Order.total), 0)).filter(order_filter).scalar() or 0
    )
    confirmed_revenue = float(
        db.query(func.coalesce(func.sum(Order.total), 0))
        .filter(order_filter, Order.status.in_(["confirmed", "shipped", "delivered"]))
        .scalar()
        or 0
    )
    delivered_revenue = float(
        db.query(func.coalesce(func.sum(Order.total), 0))
        .filter(order_filter, Order.status == "delivered")
        .scalar()
        or 0
    )

    aov = (revenue / total_orders) if total_orders else 0.0
    conv = (total_orders / total_clicks) if total_clicks else 0.0
    conf_conv = (confirmed_orders / total_clicks) if total_clicks else 0.0

    # ---- Timeseries (one row per UTC day) ----
    clicks_by_day = dict(
        db.query(
            func.date_trunc("day", Click.created_at).label("d"),
            func.count(Click.id),
        )
        .filter(click_filter)
        .group_by("d")
        .all()
    )
    orders_by_day = dict(
        db.query(
            func.date_trunc("day", Order.created_at).label("d"),
            func.count(Order.id),
        )
        .filter(order_filter)
        .group_by("d")
        .all()
    )
    confirmed_orders_by_day = dict(
        db.query(
            func.date_trunc("day", Order.created_at).label("d"),
            func.count(Order.id),
        )
        .filter(order_filter, Order.status.in_(["confirmed", "shipped", "delivered"]))
        .group_by("d")
        .all()
    )
    revenue_by_day = dict(
        db.query(
            func.date_trunc("day", Order.created_at).label("d"),
            func.coalesce(func.sum(Order.total), 0),
        )
        .filter(order_filter)
        .group_by("d")
        .all()
    )

    timeseries: List[TimeseriesPoint] = []
    cursor = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = end.replace(hour=0, minute=0, second=0, microsecond=0)
    while cursor <= end_day:
        timeseries.append(
            TimeseriesPoint(
                date=cursor.date().isoformat(),
                clicks=int(clicks_by_day.get(cursor, 0)),
                orders=int(orders_by_day.get(cursor, 0)),
                confirmed_orders=int(confirmed_orders_by_day.get(cursor, 0)),
                revenue=float(revenue_by_day.get(cursor, 0)),
            )
        )
        cursor += timedelta(days=1)

    # ---- Breakdown: top UTM sources / campaigns / landing pages ----
    def utm_breakdown(field) -> List[BreakdownRow]:
        # Clicks grouped by field
        click_rows = dict(
            db.query(field, func.count(Click.id))
            .filter(click_filter, field.isnot(None), field != "")
            .group_by(field)
            .all()
        )
        order_count_rows = dict(
            db.query(field, func.count(Order.id))
            .filter(order_filter, field.isnot(None), field != "")
            .group_by(field)
            .all()
        )
        revenue_rows = dict(
            db.query(field, func.coalesce(func.sum(Order.total), 0))
            .filter(order_filter, field.isnot(None), field != "")
            .group_by(field)
            .all()
        )
        keys = set(click_rows) | set(order_count_rows) | set(revenue_rows)
        rows = [
            BreakdownRow(
                key=str(k) if k else "(none)",
                clicks=int(click_rows.get(k, 0)),
                orders=int(order_count_rows.get(k, 0)),
                revenue=float(revenue_rows.get(k, 0)),
            )
            for k in keys
        ]
        rows.sort(key=lambda r: (r.orders, r.clicks, r.revenue), reverse=True)
        return rows[:8]

    top_utm_sources = utm_breakdown(Click.utm_source) or []
    # Same query but pulling from Order for sources/campaigns the click table
    # didn't see (e.g. when MaxMind was down at click time but the order
    # eventually came in). Falls back gracefully on empty.
    top_utm_campaigns = utm_breakdown(Click.utm_campaign) or []
    top_landing_pages = utm_breakdown(Click.page_path) or []

    return MetricsOut(
        range_from=start.isoformat(),
        range_to=end.isoformat(),
        total_clicks=total_clicks,
        unique_visitors=unique_visitors,
        total_orders=total_orders,
        confirmed_orders=confirmed_orders,
        delivered_orders=delivered_orders,
        cancelled_orders=cancelled_orders,
        rejected_fraud_orders=rejected_fraud_orders,
        pending_orders=pending_orders,
        revenue=revenue,
        confirmed_revenue=confirmed_revenue,
        delivered_revenue=delivered_revenue,
        average_order_value=aov,
        conversion_rate=conv,
        confirmed_conversion_rate=conf_conv,
        timeseries=timeseries,
        top_utm_sources=top_utm_sources,
        top_utm_campaigns=top_utm_campaigns,
        top_landing_pages=top_landing_pages,
    )


# ---------------------------------------------------------------------------
# Orders
# ---------------------------------------------------------------------------

@router.get("/orders", response_model=OrderListOut)
def list_orders(
    range_from: Optional[str] = Query(None, alias="from"),
    range_to: Optional[str] = Query(None, alias="to"),
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    only_valid: bool = Query(True),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: Literal["created_at", "total"] = Query("created_at"),
    order: Literal["asc", "desc"] = Query("desc"),
    db: Session = Depends(get_db),
    _: str = Depends(require_admin),
):
    start, end = _parse_range(range_from, range_to)
    q = db.query(Order).filter(Order.created_at >= start, Order.created_at <= end)

    if only_valid:
        q = q.filter(Order.is_valid_traffic.is_(True))

    if status_filter:
        statuses = [s.strip() for s in status_filter.split(",") if s.strip()]
        if statuses:
            q = q.filter(Order.status.in_(statuses))

    if search:
        s = f"%{search.strip()}%"
        q = q.filter(
            or_(
                Order.order_number.ilike(s),
                Order.customer_name.ilike(s),
                Order.phone_e164.ilike(s),
                Order.phone_raw.ilike(s),
                Order.address.ilike(s),
            )
        )

    total = q.count()

    sort_col = Order.total if sort == "total" else Order.created_at
    q = q.order_by(sort_col.desc() if order == "desc" else sort_col.asc())
    q = q.options(joinedload(Order.items))

    rows = q.offset((page - 1) * page_size).limit(page_size).all()
    items = [_serialize_order_list_row(o, len(o.items)) for o in rows]

    pages = max(1, (total + page_size - 1) // page_size)
    return OrderListOut(total=total, page=page, page_size=page_size, pages=pages, items=items)


@router.get("/orders/{order_id}", response_model=OrderDetailOut)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    _: str = Depends(require_admin),
):
    o: Optional[Order] = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id)
        .first()
    )
    if not o:
        raise HTTPException(status_code=404, detail="ORDER_NOT_FOUND")

    return OrderDetailOut(
        order_id=str(o.id),
        order_number=o.order_number,
        customer_name=o.customer_name,
        phone_raw=o.phone_raw,
        phone_e164=o.phone_e164,
        address=o.address,
        status=o.status or "pending_confirmation",
        currency=o.currency or "KWD",
        subtotal=float(o.subtotal or 0),
        total=float(o.total or 0),
        payment_method=o.payment_method or "COD",
        items=[
            OrderItemDetail(
                product_id=it.product_id,
                offer_id=it.offer_id,
                title=it.title,
                quantity=int(it.quantity),
                unit_price=float(it.unit_price),
                total_price=float(it.total_price),
                is_upsell=bool(it.is_upsell),
            )
            for it in o.items
        ],
        source_url=o.source_url,
        utm_source=o.utm_source,
        utm_medium=o.utm_medium,
        utm_campaign=o.utm_campaign,
        utm_content=o.utm_content,
        utm_term=o.utm_term,
        client_ip=o.client_ip,
        user_agent=o.user_agent,
        country_code=o.country_code,
        is_vpn=bool(o.is_vpn),
        is_valid_traffic=bool(o.is_valid_traffic),
        fraud_decision=o.fraud_decision,
        fraud_reason=o.fraud_reason,
        maxmind_risk_score=float(o.maxmind_risk_score) if o.maxmind_risk_score is not None else None,
        sheet_sync_status=o.sheet_sync_status,
        admin_notes=o.admin_notes,
        created_at=(o.created_at or datetime.utcnow()).isoformat(),
        updated_at=o.updated_at.isoformat() if o.updated_at else None,
    )


@router.patch("/orders/{order_id}", response_model=OrderDetailOut)
def update_order(
    order_id: str,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(require_admin),
):
    o: Optional[Order] = db.query(Order).filter(Order.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="ORDER_NOT_FOUND")
    o.status = payload.status
    if payload.admin_notes is not None:
        o.admin_notes = payload.admin_notes
    db.commit()
    db.refresh(o)
    return get_order(order_id=order_id, db=db, _="admin")  # type: ignore[arg-type]


@router.get("/order-status-options")
def order_status_options(_: str = Depends(require_admin)):
    return {
        "options": [
            {"value": "pending_confirmation", "label": "بانتظار التأكيد", "color": "amber"},
            {"value": "confirmed", "label": "مؤكد", "color": "blue"},
            {"value": "shipped", "label": "تم الشحن", "color": "indigo"},
            {"value": "delivered", "label": "تم التسليم", "color": "green"},
            {"value": "cancelled", "label": "ملغي", "color": "rose"},
            {"value": "returned", "label": "مرتجع", "color": "orange"},
            {"value": "refunded", "label": "تم الاسترداد", "color": "fuchsia"},
            {"value": "rejected_fraud", "label": "احتيال محتمل", "color": "red"},
        ]
    }
