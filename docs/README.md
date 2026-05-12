# Khafeefa Docs Pack

This folder is the build brief for a premium Arabic DTC COD store for `خفيفة / khafeefa`.

Primary market: Kuwait customers reached through TikTok, Snapchat, Meta, UGC, AI video, and edited direct-response ads.

Domains:

- Frontend: `https://getkhafeefa.shop`
- Backend API: `https://api.getkhafeefa.shop`
- Database name: `khafeefa`
- Provided internal Postgres URL: `postgres://khafeefa:khafeefa@khafeefa_database:5432/namabeauty?sslmode=disable`

Important: the connection string database segment currently says `namabeauty`. Confirm whether the real Postgres database is `khafeefa` or `namabeauty` before deploy. Do not silently change production data.

## Required Deliverable

The coder should deliver a repo with:

- `frontend/`: Next.js Arabic RTL storefront.
- `backend/`: Python FastAPI API, Postgres persistence, migrations on startup, MaxMind fraud gate, CAPI dispatch, Google Sheets webhook dispatch.
- `sheets/`: Google Apps Script webhook file and sheet CSV templates copied from `docs/templates`.
- Dockerfiles for both apps, root `docker-compose.yml` for local development, and EasyPanel-ready env examples.

## Docs Index

Read in this order:

1. `01-brand-positioning-icp.md`
2. `02-site-architecture-cro.md`
3. `03-design-system.md`
4. `04-frontend-spec.md`
5. `05-backend-spec.md`
6. `06-tracking-pixels-capi.md`
7. `07-fraud-maxmind-kuwait-only.md`
8. `08-google-sheets.md`
9. `09-deployment-env-docker.md`
10. `10-testing-qa.md`
11. `11-ai-coder-prompt.md`

## V1 Product

- Arabic name: `مروحة خصر وباور بانك في جهاز واحد`
- SKU: `khafeefa-waist-fan-powerbank`
- Offer 1: `12.900 KWD` for 1 piece
- Offer 2: `22.000 KWD` for 2 pieces
- Offer 3: `29.500 KWD` for 3 pieces

COD only. Checkout collects only name and phone number. The backend must only accept valid Kuwait numbers, with `055000000` whitelisted for production testing.

## Core Strategy

Khafeefa should not feel like a dropshipping store. It should feel like a branded Kuwait-focused comfort-tech store that curates practical products for heat, errands, family outings, work, and daily movement.

The website must create:

- Product ownership through brand naming, visual system, branded packaging mockups, SKU naming, warranty language, and quality-check language.
- Trust through COD, Kuwait-only validation, clear support, customer proof, safety notes, delivery expectations, and exchange policy.
- Authority through product testing framework, material/spec transparency, comparison against cheap generic alternatives, and evidence-backed benefits.
- Emotion through relief from heat, embarrassment, fatigue, worrying about children/parents outdoors, and the desire to look prepared.
- High AOV through tiered offers, cart cross-sells, and a time-limited post-order upsell.