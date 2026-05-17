import minfraud
from app.core.config import settings

class FraudDecision:
    def __init__(self, allowed: bool, reason: str, risk_score: float = None, response_json: dict = None):
        self.allowed = allowed
        self.reason = reason
        self.risk_score = risk_score
        self.response_json = response_json

def inspect_order(ip: str, user_agent: str, order_data: dict) -> FraudDecision:
    if not settings.MAXMIND_ACCOUNT_ID or not settings.MAXMIND_LICENSE_KEY:
        return FraudDecision(True, "MAXMIND_NOT_CONFIGURED")

    client = minfraud.Client(
        account_id=int(settings.MAXMIND_ACCOUNT_ID),
        license_key=settings.MAXMIND_LICENSE_KEY
    )

    try:
        request = {
            "device": {
                "ip_address": ip,
                "user_agent": user_agent,
            },
            "event": {
                "transaction_id": order_data.get("order_number"),
                "type": "purchase"
            },
            "billing": {
                "first_name": order_data.get("customer_name"),
            },
            "order": {
                "amount": float(order_data.get("total", 0)),
                "currency": "KWD",
            }
        }

        insights = client.insights(request)

        # Fraud signals are saved with the order, but blocking is opt-in so VPNs
        # and restricted Wi-Fi networks do not prevent cash-on-delivery orders.
        country = insights.ip_address.country.iso_code
        if country != "KW" and settings.FRAUD_BLOCK_NON_KUWAIT:
            return FraudDecision(False, "ORDER_REGION_BLOCKED", insights.risk_score, insights.dict())

        traits = insights.ip_address.traits
        uses_proxy = (
            traits.is_anonymous_vpn
            or traits.is_hosting_provider
            or traits.is_public_proxy
            or traits.is_tor_exit_node
            or traits.is_residential_proxy
        )
        if uses_proxy and settings.FRAUD_BLOCK_VPN:
            return FraudDecision(False, "VPN_OR_PROXY_BLOCKED", insights.risk_score, insights.dict())

        if insights.risk_score > settings.MAXMIND_MAX_RISK_SCORE and settings.FRAUD_BLOCK_HIGH_RISK:
            return FraudDecision(False, "HIGH_RISK_ORDER", insights.risk_score, insights.dict())

        return FraudDecision(True, "PASSED", insights.risk_score, insights.dict())

    except Exception as e:
        return FraudDecision(True, f"MAXMIND_ERROR_BYPASSED: {str(e)}")
