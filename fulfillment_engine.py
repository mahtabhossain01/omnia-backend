import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("FulfillmentEngine")

def process_customer_order(order_data):
    order_id = order_data.get("order_id", "ORD-1001")
    customer_paid = order_data.get("total_amount", 49.99)
    item = order_data.get("item", "Smart LED Strip")
    
    logger.info(f"[Fulfillment] Captured Shopify Order #{order_id} for '{item}'. Customer Paid: ${customer_paid:.2f}")
    logger.info(f"[Fulfillment] Utilizing customer funds (${customer_paid:.2f}) to trigger zero-upfront supplier fulfillment (CJ Dropshipping / AliExpress).")
    
    supplier_cost = customer_paid * 0.30 # 30% COGS
    net_profit = customer_paid - supplier_cost
    
    logger.info(f"[Fulfillment] Supplier order placed. COGS: ${supplier_cost:.2f} | Net Profit Locked: ${net_profit:.2f}")
    return {
        "order_id": order_id,
        "status": "fulfilled_customer_funded",
        "customer_paid": customer_paid,
        "supplier_cost": supplier_cost,
        "net_profit": net_profit
    }

if __name__ == "__main__":
    process_customer_order({"order_id": "ORD-9999", "total_amount": 59.99, "item": "Posture Corrector"})
