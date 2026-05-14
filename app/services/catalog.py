from decimal import Decimal

CATALOG = {
    "khafeefa-waist-fan-powerbank": {
        "title": "مروحة خفيفة للخصر مع باور بانك", # Backend uses this for the order item title
        "offers": {
            "one": {
                "quantity": 1,
                "paid_quantity": 1,
                "free_quantity": 0,
                "total_price": Decimal("12.900")
            },
            "two": {
                "quantity": 2,
                "paid_quantity": 2,
                "free_quantity": 0,
                "total_price": Decimal("22.000")
            },
            "three": {
                "quantity": 3,
                "paid_quantity": 3,
                "free_quantity": 0,
                "total_price": Decimal("29.500")
            },
            "post_order_upsell": {
                "quantity": 1,
                "paid_quantity": 1,
                "free_quantity": 0,
                "total_price": Decimal("12.900")
            }
        }
    }
}

def get_offer_details(product_id: str, offer_id: str):
    product = CATALOG.get(product_id)
    if not product:
        return None
    offer = product["offers"].get(offer_id)
    if not offer:
        return None
    
    return {
        "product_title": product["title"],
        "quantity": offer["quantity"],
        "total_price": offer["total_price"],
        "unit_price": offer["total_price"] / offer["quantity"]
    }
