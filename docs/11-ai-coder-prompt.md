# Prompt for AI Coder

Copy this prompt into the coding agent that will implement the website.

```text
You are implementing the Khafeefa DTC ecommerce store. Read every file in docs/ before coding, especially:

- docs/README.md
- docs/01-brand-positioning-icp.md
- docs/02-site-architecture-cro.md
- docs/03-design-system.md
- docs/04-frontend-spec.md
- docs/05-backend-spec.md
- docs/06-tracking-pixels-capi.md
- docs/07-fraud-maxmind-kuwait-only.md
- docs/08-google-sheets.md
- docs/09-deployment-env-docker.md
- docs/10-testing-qa.md

Build a production-ready repo with:

1. frontend/
   - Next.js App Router, TypeScript, Tailwind, Arabic RTL.
   - Premium branded design for خفيفة / khafeefa.
   - Pages: home, product landing page, collections, about, contact, thank-you, privacy, terms, refund policy, shipping policy.
   - Product: مروحة خفيفة للخصر مع باور بانك.
   - Offers:
     - 1 piece: 12.900 KWD
     - 2 pieces: 22.000 KWD
     - 3 pieces: 29.500 KWD
   - Product CTA adds selected offer to cart and opens cart drawer.
   - Cart drawer has cross-sell carousel placeholders and opens checkout popup.
   - Checkout popup has only name and Kuwait phone.
   - After successful order, show 10-15 second upsell at 12.900 KWD, then thank-you page.
   - Deferred Meta, TikTok, Snapchat web pixels with event IDs for dedup.
   - Responsive, fast, RTL correct.

2. backend/
   - Python FastAPI, Postgres, SQLAlchemy, Alembic.
   - Endpoints: health, create order, accept upsell, get public order.
   - Server-side price calculation using backend catalog.
   - Kuwait phone validation and exact test whitelist 055000000.
   - MaxMind minFraud gate: allow only Kuwait, reject suspicious/VPN/proxy/Tor/high-risk orders.
   - Meta CAPI, TikTok Events API, Snap CAPI server dispatch with SHA-256 hashed phone and shared event IDs.
   - Google Sheets webhook dispatch.
   - Event logs in DB.
   - Migrations run on backend container startup.

3. sheets/
   - Copy and use docs/templates/order-webhook.gs.
   - Copy CSV templates into sheets/ for orders, order_items, events.

4. Deployment:
   - frontend/Dockerfile
   - backend/Dockerfile
   - root docker-compose.yml
   - frontend/.env.example
   - backend/.env.example
   - README with local and EasyPanel deployment instructions.

Important constraints:

- Do not expose backend tokens in frontend.
- Do not trust frontend prices.
- Do not send raw PII in CAPI server payloads.
- Use Decimal for KWD money.
- Confirm the Postgres DB name mismatch before deploy: owner says khafeefa, provided URL ends with /namabeauty.
- Keep placeholder reviews/images clearly replaceable. Do not present fake reviews as real in code comments/content data.
- Implement tests described in docs/10-testing-qa.md.

Start by creating the repo structure, then implement frontend and backend in small commits/steps.
```

