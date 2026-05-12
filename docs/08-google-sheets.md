# Google Sheets Webhook

## Goal

Backend sends every accepted/rejected order to a Google Sheet through a Google Apps Script webhook.

Deliver:

- `sheets/order-webhook.gs`
- `sheets/orders-template.csv`
- `sheets/order_items-template.csv`
- `sheets/event_logs-template.csv`

Templates are in `docs/templates`.

## Sheet Tabs

Create these tabs exactly:

- `orders`
- `order_items`
- `events`

## Webhook Security

Google Apps Script web apps do not reliably expose custom request headers to `doPost`, so use a shared secret inside the backend-to-sheet JSON body.

Backend sends:

- JSON body with `secret: ${ORDER_WEBHOOK_SECRET}`.
- JSON body with `type`: `order_created`, `order_updated`, or `event_log`.

Apps Script checks the secret before writing. This is acceptable because only the backend knows the Apps Script webhook URL and secret. Never expose either in frontend code.

## Order Webhook Payload

```json
{
  "type": "order_created",
  "secret": "optional_if_header_not_possible",
  "order": {
    "order_id": "uuid",
    "order_number": "KH-2026-000001",
    "created_at": "2026-05-12T20:50:00Z",
    "customer_name": "string",
    "phone_e164": "+96550000000",
    "phone_raw": "50000000",
    "status": "pending_confirmation",
    "currency": "KWD",
    "subtotal": "22.000",
    "total": "22.000",
    "payment_method": "COD",
    "client_ip": "1.2.3.4",
    "country": "KW",
    "fraud_decision": "approved",
    "fraud_reason": "APPROVED",
    "maxmind_risk_score": "1.20",
    "utm_source": "tiktok",
    "utm_medium": "paid",
    "utm_campaign": "campaign",
    "utm_content": "ad",
    "utm_term": "",
    "event_id": "uuid"
  },
  "items": [
    {
      "product_id": "khafeefa-waist-fan-powerbank",
      "offer_id": "two",
      "title": "مروحة خفيفة للخصر مع باور بانك",
      "quantity": 2,
      "unit_price": "11.000",
      "total_price": "22.000",
      "is_upsell": false
    }
  ]
}
```

## Apps Script Requirements

- Parse JSON.
- Verify secret.
- Append order row to `orders`.
- Append each item row to `order_items`.
- Return JSON `{ "ok": true }`.
- Use locking to avoid row collisions.
- Never expose secret in frontend.

## Backend Behavior

- Sheet failure must not fail customer order after DB save.
- Mark `sheet_sync_status` as `sent`, `failed`, or `pending_retry`.
- Log response to `event_logs`.

