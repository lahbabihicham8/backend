# Frontend Specification

## Stack

Use:

- Next.js App Router.
- TypeScript.
- Tailwind CSS.
- shadcn/ui or Radix UI primitives for modal/dialog/accessibility.
- Zustand for cart and checkout state.
- TanStack Query for API mutations if useful.
- Zod for client validation schemas shared locally.
- Framer Motion for drawer/modal motion.
- `next/font` for fonts.

Avoid:

- Heavy UI kits that fight RTL.
- Client-only app architecture. Use server components for static content where possible.
- Pixel scripts blocking first render.

## Folder Structure

Recommended:

```text
frontend/
  app/
    layout.tsx
    page.tsx
    collections/page.tsx
    products/waist-fan-powerbank/page.tsx
    about/page.tsx
    contact/page.tsx
    thank-you/[orderId]/page.tsx
    privacy/page.tsx
    terms/page.tsx
    refund-policy/page.tsx
    shipping-policy/page.tsx
  components/
    brand/
    cart/
    checkout/
    layout/
    product/
    proof/
    tracking/
    ui/
  data/
    products.ts
    copy.ts
    reviews.ts
    faqs.ts
  lib/
    api.ts
    phone.ts
    tracking.ts
    event-id.ts
  public/
    images/placeholders/
  Dockerfile
  .env.example
```

## Environment Variables

Create `frontend/.env.example`:

```env
NEXT_PUBLIC_SITE_URL=https://getkhafeefa.shop
NEXT_PUBLIC_API_BASE_URL=https://api.getkhafeefa.shop

NEXT_PUBLIC_META_PIXEL_ID=
NEXT_PUBLIC_TIKTOK_PIXEL_ID=
NEXT_PUBLIC_SNAP_PIXEL_ID=

NEXT_PUBLIC_ENABLE_PIXELS=true
NEXT_PUBLIC_ENVIRONMENT=production
```

## Data Model

Use static product data for V1:

```ts
export const products = [
  {
    id: "khafeefa-waist-fan-powerbank",
    slug: "waist-fan-powerbank",
    brand: "خفيفة",
    title: "مروحة خفيفة للخصر مع باور بانك",
    cardTitle: "مروحة خصر وباور بانك",
    subtitle: "هواء قريب منك + شحن للطوارئ في جهاز واحد، مصمم لمشاوير الكويت والحر اليومي.",
    currency: "KWD",
    offers: [
      { id: "one", quantity: 1, price: 12.9, label: "قطعة واحدة" },
      { id: "two", quantity: 2, price: 22.0, label: "قطعتين", badge: "الأكثر طلباً" },
      { id: "three", quantity: 3, price: 29.5, label: "ثلاث قطع", badge: "أفضل قيمة" }
    ]
  }
];
```

## Cart Behavior

- Product CTA selects an offer, adds it to Zustand cart, fires `AddToCart`, and opens cart drawer.
- Cart drawer CTA opens checkout modal.
- Cross-sell carousel must support products later, but V1 can show disabled placeholders.
- Cart state should persist in `localStorage`.
- All prices display with 3 decimals for KWD: `12.900 د.ك`.

## Checkout Flow

Client-side steps:

1. Validate name and phone.
2. Normalize Kuwait phone to `+965XXXXXXXX` except whitelist test number can remain marked as test.
3. Create a unique `event_id` for InitiateCheckout and Purchase attempts.
4. POST to `POST /v1/orders`.
5. On success:
   - fire browser Purchase event with dedup event ID returned by backend if applicable.
   - show upsell modal for 10-15 seconds.
6. If upsell accepted, call `POST /v1/orders/{order_id}/upsell`.
7. Navigate to `/thank-you/[orderId]`.

Phone validation:

- Kuwait mobile numbers are 8 digits and commonly start with `5`, `6`, or `9`.
- Accept `+965XXXXXXXX`, `965XXXXXXXX`, `XXXXXXXX`.
- The explicit test whitelist is `055000000`.
- Client validation helps UX; backend is source of truth.

## API Calls

Create order request:

```json
{
  "customer_name": "string",
  "phone": "+96550000000",
  "items": [
    {
      "product_id": "khafeefa-waist-fan-powerbank",
      "offer_id": "two",
      "quantity": 2,
      "unit_price": 11.0,
      "total_price": 22.0
    }
  ],
  "currency": "KWD",
  "subtotal": 22.0,
  "total": 22.0,
  "payment_method": "COD",
  "event_id": "uuid",
  "landing_page_url": "https://getkhafeefa.shop/products/waist-fan-powerbank",
  "tracking": {
    "fbp": "...",
    "fbc": "...",
    "ttclid": "...",
    "ttp": "...",
    "sc_click_id": "...",
    "sc_cookie1": "...",
    "utm_source": "...",
    "utm_medium": "...",
    "utm_campaign": "...",
    "utm_content": "...",
    "utm_term": "..."
  }
}
```

Frontend should not send server-trusted price if avoidable. Backend must recalculate totals from its own product catalog.

## Pixel Loading

Pixels must be deferred:

- Do not block page render.
- Use Next.js `<Script strategy="afterInteractive">` or lazy load after consent/idle where applicable.
- Store click IDs and cookies for server payloads.
- All duplicated browser/server events must share the same event ID.

## Recommended Events

Browser events:

- `PageView`
- `ViewContent`
- `AddToCart`
- `InitiateCheckout`
- `Purchase`

Server events:

- `InitiateCheckout`
- `Purchase`
- optional `AddToCart` only if event IDs and timing are clean.

## Responsive Requirements

- Fully usable from iPhone-size screens.
- Sticky mobile CTA on product page.
- Cart drawer mobile full-width.
- Checkout modal mobile full-screen bottom sheet or centered panel.
- All tap targets at least 44px.

