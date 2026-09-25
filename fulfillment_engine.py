import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("FulfillmentEngine")

def process_customer_order(order_data):
    order_id = order_data.get("order_id", "ORD-1001")
    customer_paid = float(order_data.get("total_amount", 49.99))
    item = order_data.get("item", "Smart LED Strip Pro")
    is_digital = order_data.get("is_digital", False)
    
    logger.info(f"[Fulfillment] Processing Order #{order_id} for '{item}' (Digital: {is_digital}). Paid: ${customer_paid:.2f}")
    
    if is_digital:
        supplier_cost = 0.00
        shipping_info = "Instant Digital Delivery ($0 COGS)"
    else:
        supplier_cost = customer_paid * 0.30 # 30% COGS
        shipping_info = "Standard Worldwide Shipping: 10–14 Business Days"

    net_profit = customer_paid - supplier_cost
    
    logger.info(f"[Fulfillment] {shipping_info}. Supplier Cost: ${supplier_cost:.2f} | Net Profit: ${net_profit:.2f}")
    return {
        "order_id": order_id,
        "status": "fulfilled_customer_funded",
        "is_digital": is_digital,
        "customer_paid": customer_paid,
        "supplier_cost": supplier_cost,
        "net_profit": net_profit,
        "shipping": shipping_info
    }
