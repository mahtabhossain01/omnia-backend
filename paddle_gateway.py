import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("PaddleGateway")

def verify_paddle_signature(request_data, signature_header):
    # Simulated Paddle signature verification (hmac verification in production)
    logger.info("[PaddleGateway] Verifying webhook signature...")
    return True

def parse_paddle_event(payload):
    event_type = payload.get("alert_name", payload.get("event_type", "subscription_created"))
    logger.info(f"[PaddleGateway] Parsing Paddle event: {event_type}")
    
    # Extract order details
    data = payload.get("data", payload)
    order_id = data.get("order_id", data.get("checkout_id", "PADDLE-ORD-1001"))
    gross_amount = float(data.get("sale_gross", data.get("amount", 49.99)))
    item_name = data.get("product_name", data.get("item", "Smart LED Strip Pro"))
    
    return {
        "order_id": str(order_id),
        "total_amount": gross_amount,
        "item": item_name,
        "gateway": "Paddle"
    }
