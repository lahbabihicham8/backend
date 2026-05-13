# Testing and QA

## Frontend Tests

Required:

- Phone normalization unit tests.
- Cart math tests.
- Offer selection tests.
- Checkout modal validation tests.
- Pixel event ID generation tests.

Recommended tools:

- Vitest.
- Testing Library.
- Playwright for end-to-end checkout.

## Backend Tests

Required:

- Kuwait phone validation:
  - accepts `50000000`, `+96550000000`, `96550000000`.
  - rejects non-Kuwait numbers.
  - accepts whitelist numbers `55000000`, `60000000`, `90000000`.
- Order total recalculation.
- MaxMind decision rules.
- CAPI hashing:
  - Meta/TikTok E.164 hash.
  - Snap digits-only hash.
- Google Sheets payload shape.
- Upsell cannot be added twice.
- Upsell expires correctly.

## End-to-End Scenarios

1. Product offer selected.
2. Add to cart opens cart drawer.
3. Cart checkout opens modal.
4. Invalid Kuwait phone blocks submit.
5. Whitelisted `55000000`, `60000000`, and `90000000` can place test orders.
6. Successful order shows upsell modal for 10-15 seconds.
7. Accept upsell updates order total.
8. Skip upsell goes to thank-you.
9. Thank-you page shows order number and summary.
10. Google Sheet receives order rows.
11. CAPI event logs created.

## Pixel QA

Before production:

- Use Meta Test Events.
- Use TikTok Events Manager Test Events.
- Use Snap test event code.
- Confirm browser and server purchase events share the same event ID.
- Confirm no duplicate Purchase revenue is counted.
- Confirm phone hashes are never sent raw in server payload logs visible outside backend.

## Performance QA

Targets:

- Lighthouse mobile performance 80+ before pixels.
- No render-blocking marketing scripts.
- Product page LCP under 2.5s on normal 4G after images optimized.
- Images served through Next image optimization or well-sized local assets.

## RTL QA

Check:

- Header order is correct in RTL.
- Drawer opens naturally from the right unless design intentionally uses opposite.
- Arabic punctuation and price direction look correct.
- Forms align right.
- English `khafeefa` subtitle does not break layout.

## Fraud QA

Test with mocked MaxMind responses:

- Country `KW`, low risk: allow.
- Country `SA` or `US`: reject.
- `is_anonymous_vpn=true`: reject.
- `is_public_proxy=true`: reject.
- `risk_score=20`: reject if threshold is 15.
- MaxMind API failure: follow configured failure mode.
- Test phones `55000000`, `60000000`, `90000000`: allow.

