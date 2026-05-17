# Backend Specification

## Stack

Use:

- Python 3.12.
- FastAPI.
- Uvicorn/Gunicorn.
- SQLAlchemy 2.x async or SQLModel.
- Alembic migrations.
- Pydantic v2 settings and schemas.
- httpx for external APIs.
- Postgres.
- Docker.

## Folder Structure

```text
backend/
  app/
    main.py
    core/
      config.py
      logging.py
      security.py
    db/
      session.py
      models.py
      migrations/
    api/
      routes/
        health.py
        orders.py
        tracking.py
    services/
      catalog.py
      orders.py
      phone.py
      maxmind.py
      sheets.py
      capi_meta.py
      capi_tiktok.py
      capi_snap.py
      hashing.py
    schemas/
      orders.py
      tracking.py
    tests/
  alembic.ini
  Dockerfile
  .env.example
```

## Environment Variables

Create `backend/.env.example`:

```env
ENVIRONMENT=production
APP_NAME=khafeefa-api
API_BASE_URL=https://api.getkhafeefa.shop
FRONTEND_ORIGIN=https://getkhafeefa.shop
CORS_ORIGINS=https://getkhafeefa.shop

DATABASE_URL=postgres://getkhafeefa:getkhafeefa@khafeefa_database:5432/getkhafeefa?sslmode=disable
RUN_MIGRATIONS_ON_START=true

ORDER_WEBHOOK_URL=
ORDER_WEBHOOK_SECRET=

MAXMIND_ACCOUNT_ID=
MAXMIND_LICENSE_KEY=
MAXMIND_MINFRAUD_ENDPOINT=https://minfraud.maxmind.com/minfraud/v2.0/insights
MAXMIND_MAX_RISK_SCORE=15
MAXMIND_ALLOW_TEST_PHONES=55000000,60000000,90000000
ALLOW_NON_KUWAIT_IPS=false
FRAUD_API_FAILURE_MODE=reject

META_PIXEL_ID=
META_ACCESS_TOKEN=
META_TEST_EVENT_CODE=

TIKTOK_PIXEL_CODE=
TIKTOK_ACCESS_TOKEN=
TIKTOK_TEST_EVENT_CODE=

SNAP_PIXEL_ID=
SNAP_ACCESS_TOKEN=
SNAP_TEST_EVENT_CODE=

WHATSAPP_SUPPORT_NUMBER=
LOG_LEVEL=INFO
```

## Core Endpoints

### `GET /health`

Returns app and DB status.

### `POST /v1/orders`

Creates initial COD order.

Responsibilities:

1. Validate request schema.
2. Normalize and validate Kuwait phone.
3. Allow whitelisted `55000000`, `60000000`, and `90000000` for test orders.
4. Recalculate cart totals server-side from catalog.
5. Extract client IP from trusted proxy headers.
6. Run MaxMind minFraud unless test phone.
7. Reject non-Kuwait/suspicious/VPN/proxy orders.
8. Save order and fraud decision to Postgres.
9. Send Google Sheets webhook.
10. Send server-side CAPI Purchase/InitiateCheckout events.
11. Return order ID, public order number, total, status, and event IDs.

Response:

```json
{
  "order_id": "uuid",
  "order_number": "KH-2026-000001",
  "status": "pending_confirmation",
  "currency": "KWD",
  "total": 29.9,
  "event_id": "uuid",
  "upsell_expires_in_seconds": 15
}
```

### `POST /v1/orders/{order_id}/upsell`

Adds the post-order upsell item if within valid time window.

Rules:

- Only available after a successful initial order.
- Price is `18.900 KWD`.
- Only one upsell acceptance per order.
- Update order total and items.
- Send update webhook to Google Sheets.
- Send CAPI event if desired as `UpsellAccepted` custom event or additional purchase value update. Avoid double-counting purchase revenue unless measurement plan is explicit.

### `GET /v1/orders/{order_id}`

Public thank-you page lookup. Return minimal order data. Do not expose internal fraud fields.

## Database Models

### `orders`

Fields:

- `id` UUID primary key.
- `order_number` unique string.
- `customer_name`.
- `phone_raw`.
- `phone_e164`.
- `phone_is_test_whitelisted` boolean.
- `currency`.
- `subtotal`.
- `total`.
- `payment_method` default `COD`.
- `status`: `pending_confirmation`, `rejected_fraud`, `cancelled`, `confirmed`, `delivered`.
- `source_url`.
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`.
- `fbp`, `fbc`, `ttclid`, `ttp`, `sc_click_id`, `sc_cookie1`.
- `client_ip`.
- `user_agent`.
- `event_id`.
- `fraud_decision`.
- `fraud_reason`.
- `maxmind_risk_score`.
- `maxmind_response_json`.
- `sheet_sync_status`.
- `created_at`, `updated_at`.

### `order_items`

- `id` UUID.
- `order_id`.
- `product_id`.
- `offer_id`.
- `title`.
- `quantity`.
- `unit_price`.
- `total_price`.
- `is_upsell`.
- `created_at`.

### `event_logs`

- `id`.
- `order_id`.
- `platform`: `meta`, `tiktok`, `snap`, `sheets`.
- `event_name`.
- `event_id`.
- `request_json`.
- `response_json`.
- `status_code`.
- `success`.
- `created_at`.

## Catalog

Keep V1 catalog in backend code/config, not in frontend only.

Offer totals:

- `one`: quantity 1, paid quantity 1, free quantity 0, total `18.900`.
- `buy2get1`: quantity 3, paid quantity 2, free quantity 1, total `29.900`.
- `post_order_upsell`: quantity 1, total `18.900`.

Product specs to expose through backend catalog if needed:

- Battery: `4000mAh`.
- Wind speeds: `5`.
- Charging: USB rechargeable.
- Voltage/power: `5V`, `5W`.
- Dimensions: `88 x 115 x 53 mm`.
- Public working-time copy: `حتى 8 ساعات حسب السرعة وطريقة الاستخدام`.
- Supplier-listed certificates: FCC, KC, CE, RoHS. Store these internally as unverified until actual certificates for the sold batch are available.

Use Decimal for money, never binary float in calculations.

## Migrations on Startup

Container startup command should run:

```bash
alembic upgrade head && gunicorn app.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

If using a Python entrypoint script, make migration failure fail the container loudly.

## CORS and Proxy

- Allow only `https://getkhafeefa.shop` in production.
- Configure trusted proxy behavior for EasyPanel/reverse proxy so `X-Forwarded-For` is parsed correctly.
- Never trust arbitrary client-sent IP fields from JSON.

## Error Handling

Return friendly Arabic-safe error codes:

- `INVALID_PHONE`
- `NON_KUWAIT_PHONE`
- `ORDER_REGION_BLOCKED`
- `VPN_OR_PROXY_BLOCKED`
- `HIGH_RISK_ORDER`
- `PRODUCT_UNAVAILABLE`
- `UPSELL_EXPIRED`

Frontend maps these to Arabic copy.

