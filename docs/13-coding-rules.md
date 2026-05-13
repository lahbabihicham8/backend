# Coding Rules for AI Coder

These rules are part of the implementation brief. Follow them unless a later business decision explicitly changes the product or stack.

## Product and Pricing Rules

- The backend is the source of truth for catalog, offers, quantities, totals, and upsell eligibility.
- Do not trust frontend prices, quantities, discounts, or order totals.
- Use `Decimal` for all KWD money in the backend.
- Display prices with three decimals: `18.900 د.ك`.
- V1 offers:
  - `one`: 1 piece, `18.900 KWD`.
  - `buy2get1`: 3 total pieces, `29.900 KWD`, positioned as `Buy 2, get 1 free`.
  - `post_order_upsell`: relevant product/item, `18.900 KWD`, only shown after a valid order for 10-15 seconds.

## Frontend Rules

- Use Next.js App Router, TypeScript, Tailwind CSS, and Arabic RTL from the root layout.
- Use `lang="ar-KW"` and `dir="rtl"`.
- Prefer server components for static marketing sections and client components only for cart, checkout, timers, and pixels.
- Use Zustand or a small local store for cart state.
- Use Radix UI or shadcn/ui primitives for accessible dialogs, drawers, accordions, and focus traps.
- Use local placeholder images/SVGs in `public/images/placeholders`; do not depend on external placeholder services.
- Load marketing pixels after first interaction or `afterInteractive`; never block LCP.
- Keep mobile checkout thumb-friendly: large buttons, minimal fields, sticky CTA on product page.

## Backend Rules

- Use FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, Postgres, and httpx.
- Run database migrations on container startup and fail loudly if migrations fail.
- Keep secrets only in backend environment variables.
- Implement CORS for `https://getkhafeefa.shop` only in production.
- Add rate limiting to `POST /v1/orders`.
- Extract the real client IP from trusted proxy headers configured for EasyPanel; never trust a JSON field from the browser as the IP.
- Save rejected fraud attempts when possible so the sheet and DB show fake-order patterns.

## Phone and Fraud Rules

- Real Kuwait mobile numbers are 8 local digits and should start with `5`, `6`, or `9`.
- Accept input formats `XXXXXXXX`, `965XXXXXXXX`, and `+965XXXXXXXX`.
- Normalize valid real numbers to E.164: `+965XXXXXXXX`.
- Test whitelist numbers are `55000000`, `60000000`, and `90000000`; formatted variants that normalize to those local digits may pass.
- For non-test orders, call MaxMind minFraud before accepting the order.
- Reject non-Kuwait IPs, anonymous IPs, VPN, public proxy, residential proxy, hosting provider, Tor, high-risk country, or risk score above `MAXMIND_MAX_RISK_SCORE`.
- Default `FRAUD_API_FAILURE_MODE` should be `reject` unless a manual-review process is implemented.

## Tracking Rules

- Generate one stable `event_id` per deduped conversion action.
- Browser and server Purchase events must use the same `event_id`.
- Do not expose Meta, TikTok, or Snap access tokens in frontend code.
- Server-side CAPI must hash phone numbers with SHA-256 before sending.
- Meta and TikTok phone hash should use the normalized E.164 value consistently.
- Snapchat phone hash should use digits only with country code, no plus sign.
- Include click IDs and first-party cookies when available: `_fbp`, `_fbc`, `ttclid`, `_ttp`, `ScCid`, `_scid`, UTMs.
- Log all CAPI requests and responses with tokens redacted. CAPI failure must not fail a successfully saved customer order.

## Content and Trust Rules

- Do not say or imply Khafeefa manufactures the product unless that becomes true.
- Do make the store feel like it owns the customer experience: brand selection, quality check, packaging, support, COD, warranty language.
- Do not invent real reviews, sales counts, certifications, or government approvals.
- Placeholder reviews/video slots must be labeled as placeholders in code/content until replaced with real UGC.
- Avoid medical claims like preventing heatstroke, treating sweating, or curing fatigue.
- Use proof-backed language: airflow supports perceived cooling, hands-free design helps during movement, power bank is for emergency convenience.
- Supplier-listed product claims such as `4000mAh`, `5 wind speeds`, `FCC`, `KC`, `CE`, and `RoHS` must be modeled in content as supplier data. Only display certification badges publicly after certificates are verified for the exact batch/model.

## Testing Rules

- Add frontend tests for phone parsing, cart math, offer selection, checkout validation, and event ID generation.
- Add backend tests for phone normalization, whitelist behavior, MaxMind decisions, order recalculation, CAPI hashing, Sheets payloads, and upsell expiration.
- Add at least one Playwright happy path: product page -> add bundle -> cart -> checkout -> upsell skip/accept -> thank-you.
- Mock external APIs in tests.

## Deployment Rules

- Deliver `frontend/Dockerfile`, `backend/Dockerfile`, and root `docker-compose.yml`.
- Deliver `frontend/.env.example` and `backend/.env.example`.
- Do not commit production `.env` files or real API keys.
- The backend production `DATABASE_URL` belongs only in EasyPanel env vars.
- Health endpoint must verify app and DB connectivity.

