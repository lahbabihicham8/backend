# Tracking, Web Pixels, and CAPI

## Goals

Track events across Meta, TikTok, and Snapchat with:

- Deferred browser pixels for speed.
- Server-side CAPI for conversion recovery.
- Shared event IDs for deduplication.
- Correct phone hashing server-side.
- Click IDs and first-party IDs passed from browser to backend.

## Events

Implement:

- `PageView`
- `ViewContent`
- `AddToCart`
- `InitiateCheckout`
- `Purchase`
- Optional custom: `UpsellAccepted`

Deduped events:

- If both browser and server send the same event, use the same `event_id`.
- Most important: `Purchase`.
- TikTok requires `event_id` on both Pixel and Events API for deduplication and deduplicates identical event/event_id within its dedup window.
- Snap recommends `event_id` on all integrations; for Snap Pixel, event ID maps to `client_dedup_id` for non-purchase and `transaction_id` for purchase.
- Meta uses browser/server event dedup through matching event name and event ID.

## Browser Pixel Loading

Use Next.js scripts with `strategy="afterInteractive"` or load on idle after first paint.

Do not:

- Block page render with pixels.
- Put access tokens in frontend.
- Send unhashed PII from browser unless official pixel advanced matching is intentionally configured.

Do:

- Store URL params in first-party cookies/localStorage:
  - `fbclid` and derived `_fbc` if needed.
  - `_fbp`.
  - `ttclid`.
  - `_ttp`.
  - `ScCid`.
  - `_scid`.
  - UTMs.
- Send these to backend with the order payload.

## Phone Normalization and Hashing

Backend hashing helper:

- `sha256_hex(value: str) -> str`
- Always lowercase hex output.

Meta:

- Normalize phone to E.164 format before hashing, e.g. `+96550000000`.
- Hash with SHA-256.
- Put in `user_data.ph`.

TikTok:

- Use SHA-256 hashed phone.
- Normalize to E.164 for internal consistency. For raw TikTok web advanced matching, E.164 uses `+{country}{number}`.
- For server hashed value, hash the normalized phone string consistently. Document the exact implementation in code comments.
- Include `ttclid`, `_ttp`, IP, user agent, and `event_id`.

Snapchat:

- Snap docs say phone normalization should include country code, remove double `00`, remove leading `0`, and exclude non-numeric characters including `+`.
- For Snap `ph`, hash digits-only format, e.g. `96550000000`.
- Include `client_ip_address`, `client_user_agent`, `sc_click_id`, `sc_cookie1`, `event_id`.

## Meta CAPI Payload Shape

Endpoint:

`https://graph.facebook.com/vXX.X/{META_PIXEL_ID}/events?access_token={META_ACCESS_TOKEN}`

Payload example:

```json
{
  "data": [
    {
      "event_name": "Purchase",
      "event_time": 1778610000,
      "event_id": "uuid",
      "action_source": "website",
      "event_source_url": "https://getkhafeefa.shop/products/waist-fan-powerbank",
      "user_data": {
        "ph": ["sha256_e164_phone"],
        "client_ip_address": "1.2.3.4",
        "client_user_agent": "Mozilla/5.0",
        "fbp": "fb.1...",
        "fbc": "fb.1..."
      },
      "custom_data": {
        "currency": "KWD",
        "value": 22.0,
        "content_ids": ["khafeefa-waist-fan-powerbank"],
        "content_type": "product",
        "contents": [
          { "id": "khafeefa-waist-fan-powerbank", "quantity": 2, "item_price": 11.0 }
        ],
        "order_id": "KH-2026-000001"
      }
    }
  ],
  "test_event_code": "optional"
}
```

## TikTok Events API Payload Shape

Use the current TikTok Business API docs while implementing, but the service should support this shape:

```json
{
  "event_source": "web",
  "event_source_id": "TIKTOK_PIXEL_CODE",
  "data": [
    {
      "event": "CompletePayment",
      "event_time": 1778610000,
      "event_id": "uuid",
      "user": {
        "ttclid": "ttclid",
        "ttp": "_ttp",
        "phone": "sha256_e164_phone",
        "ip": "1.2.3.4",
        "user_agent": "Mozilla/5.0"
      },
      "properties": {
        "currency": "KWD",
        "value": 22.0,
        "content_type": "product",
        "contents": [
          {
            "content_id": "khafeefa-waist-fan-powerbank",
            "content_name": "مروحة خفيفة للخصر مع باور بانك",
            "quantity": 2,
            "price": 11.0
          }
        ],
        "order_id": "KH-2026-000001"
      },
      "page": {
        "url": "https://getkhafeefa.shop/products/waist-fan-powerbank"
      }
    }
  ]
}
```

Map events:

- `ViewContent` -> `ViewContent`
- `AddToCart` -> `AddToCart`
- `InitiateCheckout` -> `InitiateCheckout`
- `Purchase` -> `CompletePayment`

## Snapchat CAPI Payload Shape

Payload example:

```json
{
  "data": [
    {
      "event_name": "PURCHASE",
      "event_time": 1778610000000,
      "event_source_url": "https://getkhafeefa.shop/products/waist-fan-powerbank",
      "event_id": "uuid",
      "action_source": "WEB",
      "user_data": {
        "ph": "sha256_digits_only_phone",
        "client_ip_address": "1.2.3.4",
        "client_user_agent": "Mozilla/5.0",
        "sc_click_id": "ScCid",
        "sc_cookie1": "_scid"
      },
      "custom_data": {
        "currency": "KWD",
        "value": 22.0,
        "content_ids": ["khafeefa-waist-fan-powerbank"],
        "content_name": "مروحة خفيفة للخصر مع باور بانك",
        "content_type": "product",
        "num_items": "2",
        "order_id": "KH-2026-000001"
      }
    }
  ],
  "test_event_code": "optional"
}
```

Snap phone hashing reminder:

- Input `+965 5000 0000`.
- Normalize to `96550000000`.
- SHA-256 hash.

## Event Logging

Every server event dispatch must be logged to `event_logs`.

Store:

- platform.
- event name.
- event ID.
- request JSON with tokens redacted.
- response status/body.
- success boolean.

Failed CAPI must not fail the customer order. Retry can be added later, but V1 should log failures.

## Consent and Legal

Add privacy policy language saying the store uses cookies/pixels for measurement and order confirmation. If targeting regions with stricter consent requirements later, add consent management before firing marketing pixels.

