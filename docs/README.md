# Khafeefa Docs Pack

This folder is the build brief for a premium Arabic DTC COD store for `خفيفة / khafeefa`.

Primary market: Kuwait customers reached through TikTok, Snapchat, Meta, UGC, AI video, and edited direct-response ads.

Domains:

- Frontend: `https://getkhafeefa.shop`
- Backend API: `https://api.getkhafeefa.shop`
- Database name: `getkhafeefa`
- Backend Postgres URL: `postgres://getkhafeefa:getkhafeefa@khafeefa_database:5432/getkhafeefa?sslmode=disable`

Keep the real `DATABASE_URL` in `backend/.env`; do not commit production credentials.

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
11. `12-arabic-copy-cro-bank.md`
12. `13-coding-rules.md`
13. `11-ai-coder-prompt.md`

## V1 Product

- Arabic name: `مروحة خصر وباور بانك في جهاز واحد`
- SKU: `khafeefa-waist-fan-powerbank`
- Offer 1: `18.900 KWD` for 1 piece
- Offer 2: `29.900 KWD` for 3 pieces total, positioned as `Buy 2, get 1 free`

COD only. Checkout collects only name and phone number. The backend must only accept valid Kuwait mobile numbers and Kuwait IPs that pass MaxMind minFraud checks. Test phones `55000000`, `60000000`, and `90000000` are whitelisted for production testing.

## Core Strategy

Khafeefa should not feel like a dropshipping store. It should feel like a branded Kuwait-focused comfort-tech store that curates practical products for heat, errands, family outings, work, and daily movement.

The website must create:

- Product ownership through brand naming, visual system, branded packaging mockups, SKU naming, warranty language, and quality-check language.
- Trust through COD, Kuwait-only validation, clear support, customer proof, safety notes, delivery expectations, and exchange policy.
- Authority through product testing framework, material/spec transparency, comparison against cheap generic alternatives, and evidence-backed benefits.
- Emotion through relief from heat, embarrassment, fatigue, worrying about children/parents outdoors, and the desire to look prepared.
- High AOV through tiered offers, cart cross-sells, and a time-limited post-order upsell.