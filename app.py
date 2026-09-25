import os
import threading
import time
import glob
from flask import Flask, jsonify, request, render_template_string, send_from_directory
from dropshipping_agent import run_autonomous_loop
from organic_marketing_agent import generate_vertical_short_video
from fulfillment_engine import process_customer_order
from payout_router import record_transaction, get_analytics
from paddle_gateway import verify_paddle_signature, parse_paddle_event

app = Flask(__name__, static_folder='static')

BASE_HTML_WRAPPER = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Omnia Store</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; background: #f9f9f9; }
        header { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
        h1 { color: #111; margin: 0; font-size: 1.5rem; }
        .content { background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        footer { margin-top: 30px; text-align: center; font-size: 0.85rem; color: #666; border-top: 1px solid #eee; padding-top: 15px; }
        footer a { color: #0066cc; text-decoration: none; margin: 0 10px; }
        footer a:hover { text-decoration: underline; }
        .btn { display: inline-block; background: #0066cc; color: #fff; padding: 10px 20px; border-radius: 4px; text-decoration: none; font-weight: 600; margin-top: 15px; }
        .btn:hover { background: #0055b3; }
    </style>
</head>
<body>
    <header>
        <h1>Omnia Global Store</h1>
        <nav><a href="/">Home</a> | <a href="/analytics">Analytics</a> | <a href="/payouts">Payouts</a></nav>
    </header>
    <div class="content">
        <h2>{{ title }}</h2>
        {{ body|safe }}
    </div>
    <footer>
        <p>&copy; 2026 Omnia Systems. All rights reserved. | Standard Worldwide Shipping: 10–14 Business Days</p>
        <div>
            <a href="/privacy-policy">Privacy Policy</a>
            <a href="/refund-policy">Refund Policy</a>
            <a href="/terms-of-service">Terms of Service</a>
            <a href="/contact-us">Contact Us</a>
        </div>
    </footer>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(BASE_HTML_WRAPPER, title="Welcome to Omnia", body='''
        <p>Welcome to Omnia — your automated zero-capital e-commerce & digital asset hub.</p>
        <p><strong>Shipping Notice:</strong> Standard Worldwide Shipping: 10–14 Business Days.</p>
        <a href="/digital-product" class="btn">Explore Instant Digital Product ($0 COGS)</a>
        <br><br>
        <a href="/analytics" class="btn" style="background: #28a745;">View Live Business Analytics</a>
    ''')

@app.route('/digital-product')
def digital_product():
    return render_template_string(BASE_HTML_WRAPPER, title="Omnia Viral Growth Masterclass (Digital)", body='''
        <p>Instant Digital Download — Zero Wait Time, $0 COGS, Instant Global Fulfillment.</p>
        <p><strong>Price:</strong> $29.99 USD</p>
        <p>Includes complete viral UGC video templates, automated dropshipping guides, and Paddle/Payoneer setup checklists.</p>
        <form action="/webhook/paddle" method="POST">
            <input type="hidden" name="alert_name" value="payment_succeeded">
            <input type="hidden" name="order_id" value="DIGITAL-'''+str(int(time.time()))+'''">
            <input type="hidden" name="sale_gross" value="29.99">
            <input type="hidden" name="product_name" value="Omnia Viral Growth Masterclass">
            <input type="hidden" name="is_digital" value="true">
            <button type="submit" class="btn">Buy Now with Paddle (Instant Access)</button>
        </form>
    ''')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template_string(BASE_HTML_WRAPPER, title="Privacy Policy", body='''
        <p>Effective date: January 1, 2026</p>
        <p>Omnia ("we", "our", or "us") operates the Omnia global store. This Privacy Policy explains how we collect, use, and protect your personal information when you visit our website or make a purchase.</p>
        <h3>Information We Collect</h3>
        <p>When you make a purchase, we collect your name, email address, shipping address, and payment details processed securely via Paddle (Merchant of Record).</p>
        <h3>Use of Information</h3>
        <p>We use your information exclusively to fulfill physical or digital orders, provide customer support, and process automated payouts via Payoneer.</p>
    ''')

@app.route('/refund-policy')
def refund_policy():
    return render_template_string(BASE_HTML_WRAPPER, title="Refund Policy", body='''
        <p>At Omnia, we want you to be completely satisfied with your purchase.</p>
        <h3>Physical Goods</h3>
        <p>Due to our direct-to-supplier automated routing, refund requests for physical items must be initiated within 14 days of delivery. Standard worldwide shipping takes 10–14 business days.</p>
        <h3>Digital Goods</h3>
        <p>Digital masterclasses and downloadable assets are delivered instantly and are non-refundable once downloaded.</p>
    ''')

@app.route('/terms-of-service')
def terms_of_service():
    return render_template_string(BASE_HTML_WRAPPER, title="Terms of Service", body='''
        <p>Welcome to Omnia. By accessing our website and purchasing our products, you agree to abide by the following terms and conditions.</p>
        <h3>1. Purchases & Billing</h3>
        <p>All payments are processed securely by Paddle as our Merchant of Record. Prices are listed in USD and subject to applicable taxes.</p>
        <h3>2. Shipping & Fulfillment</h3>
        <p>Physical orders are fulfilled automatically via global suppliers with standard worldwide shipping taking 10–14 business days.</p>
    ''')

@app.route('/contact-us')
def contact_us():
    return render_template_string(BASE_HTML_WRAPPER, title="Contact Us", body='''
        <p>Have questions about your order, shipping, or digital downloads? We are here 24/7 to help.</p>
        <p><strong>Email Support:</strong> support@omniasystem.org</p>
        <p><strong>Response Time:</strong> Within 4 hours (Automated AI Support Desk)</p>
    ''')

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
        "receiving_email": os.environ.get("PAYONEER_RECEIVING_EMAIL", "mahtabhossain2nt7@gmail.com"),
        "net_profit_balance": data["net_profit"],
        "transactions": data["transactions"]
    })

@app.route('/static/media/<path:filename>')
def serve_media(filename):
    media_dir = os.path.join(os.path.dirname(__file__), 'static', 'media')
    return send_from_directory(media_dir, filename)

@app.route('/webhook/paddle', methods=['POST'])
def paddle_webhook():
    # Support both form-urlencoded (Paddle standard) and JSON
    payload = request.form.to_dict() or request.json or {}
    
    # Check if digital
    is_digital = payload.get("is_digital") == "true" or payload.get("is_digital") is True
    
    parsed_event = parse_paddle_event(payload)
    parsed_event["is_digital"] = is_digital
    
    fulfillment_result = process_customer_order(parsed_event)
    record_transaction(fulfillment_result)
    
    return jsonify({
        "status": "success",
        "gateway": "Paddle",
        "event": parsed_event,
        "fulfillment": fulfillment_result
    }), 200

def cleanup_old_media():
    # Auto-clean temporary media files older than 24 hours to prevent storage limits
    media_dir = os.path.join(os.path.dirname(__file__), 'static', 'media')
    now = time.time()
    for f in glob.glob(os.path.join(media_dir, "*.*")):
        if os.stat(f).st_mtime < now - 86400:
            try:
                os.remove(f)
                print(f"[Cleanup] Removed old media file: {f}")
            except Exception as e:
                print(f"[Cleanup Error] {e}")

def start_background_agent():
    print("[Flask] Starting background media cleanup routine...")
    while True:
        try:
            cleanup_old_media()
        except Exception as e:
            print(f"Cleanup error: {e}")
        time.sleep(3600)

if __name__ == '__main__':
    agent_thread = threading.Thread(target=start_background_agent, daemon=True)
    agent_thread.start()
    
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port)
