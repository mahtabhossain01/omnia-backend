import os
import threading
import time
from flask import Flask, jsonify, request
from dropshipping_agent import run_autonomous_loop
from organic_marketing_agent import generate_vertical_short_video
from fulfillment_engine import process_customer_order
from payout_router import record_transaction, get_analytics
from paddle_gateway import verify_paddle_signature, parse_paddle_event

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "system": "Omnia Zero-Capital Dropshipping & Paddle Live Billing Pipeline",
        "paddle_environment": os.environ.get("PADDLE_ENVIRONMENT", "live"),
        "active_thread": agent_thread.is_alive() if 'agent_thread' in globals() else False
    })

@app.route('/ping')
def ping():
    return "pong", 200

@app.route('/status')
def status():
    return jsonify({
        "status": "running",
        "timestamp": time.time(),
        "analytics": get_analytics()
    })

@app.route('/analytics')
def analytics():
    return jsonify(get_analytics())

@app.route('/payouts')
def payouts():
    data = get_analytics()
    return jsonify({
        "payout_gateway": "Payoneer (Auto-Payout Configured)",
        "receiving_email": os.environ.get("PAYONEER_RECEIVING_EMAIL", "your-payoneer-email@domain.com"),
        "net_profit_balance": data["net_profit"],
        "transactions": data["transactions"]
    })

@app.route('/webhook/paddle', methods=['POST'])
def paddle_webhook():
    payload = request.form.to_dict() or request.json or {}
    sig = request.headers.get("Paddle-Signature", "")
    
    if not verify_paddle_signature(payload, sig):
        return jsonify({"status": "error", "message": "Invalid signature"}), 403
    
    parsed_event = parse_paddle_event(payload)
    fulfillment_result = process_customer_order(parsed_event)
    record_transaction(fulfillment_result)
    
    return jsonify({
        "status": "success",
        "gateway": "Paddle",
        "event": parsed_event,
        "fulfillment": fulfillment_result
    }), 200

def start_background_agent():
    print("[Flask] Starting background dropshipping agent thread...")
    run_autonomous_loop()

if __name__ == '__main__':
    agent_thread = threading.Thread(target=start_background_agent, daemon=True)
    agent_thread.start()
    
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port)
