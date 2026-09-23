import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("PayoutRouter")

TRANSACTION_LOGS = []

def record_transaction(order_result):
    gross = order_result['customer_paid']
    # Paddle fee: ~5% + $0.50
    paddle_fee = round((gross * 0.05) + 0.50, 2)
    cogs = order_result.get('supplier_cost', gross * 0.30)
    net_profit = round(gross - (paddle_fee + cogs), 2)
    
    order_result['paddle_fee'] = paddle_fee
    order_result['supplier_cost'] = round(cogs, 2)
    order_result['net_profit'] = net_profit
    
    TRANSACTION_LOGS.append(order_result)
    logger.info(f"[PayoutRouter] Recorded Paddle Tx {order_result['order_id']} | Gross: ${gross:.2f} | Fee: ${paddle_fee:.2f} | COGS: ${cogs:.2f} | Net: ${net_profit:.2f}")

def get_analytics():
    total_revenue = sum(t['customer_paid'] for t in TRANSACTION_LOGS)
    total_fees = sum(t.get('paddle_fee', 0) for t in TRANSACTION_LOGS)
    total_cogs = sum(t['supplier_cost'] for t in TRANSACTION_LOGS)
    total_profit = sum(t['net_profit'] for t in TRANSACTION_LOGS)
    return {
        "total_orders": len(TRANSACTION_LOGS),
        "gross_revenue": round(total_revenue, 2),
        "total_paddle_fees": round(total_fees, 2),
        "total_cogs": round(total_cogs, 2),
        "net_profit": round(total_profit, 2),
        "transactions": TRANSACTION_LOGS
    }
