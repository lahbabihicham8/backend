# Fraud Gate: Kuwait Only with MaxMind

## Goal

Only allow orders that look like real Kuwait COD orders:

- Valid Kuwait phone.
- IP geolocated to Kuwait.
- Not suspicious.
- Not anonymous VPN/proxy/Tor/hosting/residential proxy.
- Test number `055000000` is whitelisted so production tests can pass.

## MaxMind Product

Use MaxMind minFraud Insights API if available.

Docs confirm relevant response fields:

- `risk_score`: decimal risk score.
- `ip_address.country.iso_code`.
- `ip_address.country.is_high_risk`.
- `ip_address.risk`.
- `ip_address.traits.is_anonymous`.
- `ip_address.traits.is_anonymous_vpn`.
- `ip_address.traits.is_hosting_provider`.
- `ip_address.traits.is_public_proxy`.
- `ip_address.traits.is_residential_proxy`.
- `ip_address.traits.is_tor_exit_node`.
- `risk_score_reasons`, including `ANONYMOUS_IP`.

## Request Data

Send MaxMind:

- Device IP from trusted reverse proxy header.
- User agent.
- Billing/shipping country as `KW`.
- Phone country as `KW` when parsed as Kuwait.
- Order amount and currency.
- Session/order ID.

Do not trust frontend-sent IP.

## Decision Rules

Bypass rules:

- If normalized raw input equals `055000000`, allow as test order.
- Mark `phone_is_test_whitelisted=true`.
- Still store IP and tracking data, but do not block.

Hard reject:

- Phone is not valid Kuwait mobile.
- MaxMind country ISO is present and not `KW`.
- `is_anonymous` true.
- `is_anonymous_vpn` true.
- `is_public_proxy` true.
- `is_residential_proxy` true.
- `is_hosting_provider` true.
- `is_tor_exit_node` true.
- `risk_score >= MAXMIND_MAX_RISK_SCORE` default `15`.
- `country.is_high_risk` true.

Soft review option:

- V1 can reject hard to reduce fake COD orders.
- Later add `manual_review` if business wants more volume.

## Error Copy

Frontend Arabic messages:

- Invalid phone:
  `رقم الهاتف غير صحيح. يرجى إدخال رقم كويتي صحيح.`
- Region blocked:
  `حالياً نستقبل الطلبات من داخل الكويت فقط.`
- VPN/proxy:
  `لإتمام الطلب، يرجى إيقاف الـ VPN أو البروكسي والمحاولة مرة أخرى.`
- High risk:
  `تعذر تأكيد الطلب تلقائياً. تواصل معنا عبر واتساب للمساعدة.`

## Phone Validation

Accepted real numbers:

- `50000000`
- `65000000`
- `95000000`
- `+96550000000`
- `96550000000`

Rejected:

- Less/more than 8 local digits.
- Non-Kuwait country codes.
- Landline prefixes if not intended for mobile COD confirmation.

Whitelist:

- Exact test input `055000000`.
- Also allow normalized variants only if explicitly desired. Default: exact raw input only to avoid accidentally allowing fake patterns.

## Implementation Pseudocode

```python
def validate_order_region(phone_raw, client_ip, user_agent, order):
    if phone_raw == settings.MAXMIND_ALLOW_TEST_PHONE:
        return FraudDecision(allowed=True, reason="TEST_PHONE_WHITELIST")

    phone = normalize_kuwait_phone(phone_raw)
    if not phone.valid:
        return FraudDecision(False, "INVALID_KUWAIT_PHONE")

    result = maxmind.inspect(ip=client_ip, user_agent=user_agent, order=order)

    country = result.ip_address.country.iso_code
    traits = result.ip_address.traits
    risk_score = result.risk_score or 0

    if country and country != "KW":
        return FraudDecision(False, "NON_KUWAIT_IP")

    if any([
        traits.is_anonymous,
        traits.is_anonymous_vpn,
        traits.is_public_proxy,
        traits.is_residential_proxy,
        traits.is_hosting_provider,
        traits.is_tor_exit_node,
    ]):
        return FraudDecision(False, "ANONYMOUS_IP")

    if risk_score >= settings.MAXMIND_MAX_RISK_SCORE:
        return FraudDecision(False, "HIGH_RISK_SCORE")

    return FraudDecision(True, "APPROVED")
```

## Operational Notes

- Log every MaxMind response for rejected and accepted orders.
- Redact secrets.
- Add admin-visible reason in Google Sheet.
- If MaxMind API fails:
  - Production default should be reject or manual-review, not blindly accept.
  - For V1, choose `manual_review` only if there is a human confirmation process.
  - Document the selected behavior in `.env.example` with `FRAUD_API_FAILURE_MODE=reject`.

