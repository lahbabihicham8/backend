"""Public click / page-view tracking endpoint.

Frontend fires `POST /v1/track/click` once per page-view. The backend looks
up the visitor IP via MaxMind, classifies it as valid or invalid traffic
(only allowed countries + non-VPN/proxy = valid), and persists a Click row.

Invalid traffic is silently dropped — the response is always 204 so client
code stays simple and bots/VPN visitors don't learn they're being filtered.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Request, Response, status
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models import Click
from app.db.session import get_db
from app.services.maxmind import lookup_ip, is_valid_traffic


router = APIRouter()


class ClickIn(BaseModel):
    session_id: str
    visitor_id: Optional[str] = None
    landing_page_url: Optional[str] = None
    page_path: Optional[str] = None
    referrer: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None
    fbp: Optional[str] = None
    fbc: Optional[str] = None
    ttclid: Optional[str] = None
    sc_click_id: Optional[str] = None


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("X-Forwarded-For")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else ""


@router.post("/click", status_code=status.HTTP_204_NO_CONTENT)
def record_click(
    payload: ClickIn,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    ip = _client_ip(request)
    ua = request.headers.get("User-Agent", "")

    lookup = lookup_ip(ip, ua)
    valid = is_valid_traffic(lookup)

    if not valid:
        # Silently drop — keep dashboard numbers clean.
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    click = Click(
        session_id=payload.session_id,
        visitor_id=payload.visitor_id,
        client_ip=ip,
        user_agent=ua,
        referrer=payload.referrer,
        landing_page_url=payload.landing_page_url,
        page_path=payload.page_path,
        country_code=(lookup.country_code or "").upper() or None,
        is_vpn=bool(lookup.is_vpn or lookup.is_proxy or lookup.is_hosting),
        is_valid_traffic=True,
        maxmind_risk_score=lookup.risk_score,
        utm_source=payload.utm_source,
        utm_medium=payload.utm_medium,
        utm_campaign=payload.utm_campaign,
        utm_content=payload.utm_content,
        utm_term=payload.utm_term,
        fbp=payload.fbp,
        fbc=payload.fbc,
        ttclid=payload.ttclid,
        sc_click_id=payload.sc_click_id,
    )
    try:
        db.add(click)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        # Don't surface the error to the client — tracking is best-effort.
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
