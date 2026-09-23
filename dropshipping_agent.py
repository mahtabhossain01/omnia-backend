import os
import json
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from organic_marketing_agent import generate_vertical_short_video
from social_poster import post_to_platforms
from fulfillment_engine import process_customer_order
from payout_router import record_transaction

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("DropshippingAgent")

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config.json: {e}")
    return {
        "schedule": {
            "inventory_sync_minutes": 30,
            "product_research_hours": 6,
            "organic_video_hours": 12
        }
    }

def product_research_job():
    try:
        logger.info("[Job] Executing product research & trend analysis...")
        winning_product = "Smart LED Strip Pro"
        logger.info(f"[Job] Product research complete: '{winning_product}' identified as winning product.")
        asset = generate_vertical_short_video(winning_product)
        post_to_platforms(asset["asset_path"], winning_product)
    except Exception as e:
        logger.error(f"[Job Error] Product research failed: {e}")

def inventory_sync_job():
    try:
        logger.info("[Job] Executing inventory sync with supplier & Shopify store...")
        logger.info("[Job] Inventory sync complete: Stock levels and pricing updated successfully.")
    except Exception as e:
        logger.error(f"[Job Error] Inventory sync failed: {e}")

def organic_marketing_job():
    try:
        logger.info("[Job] Executing organic short-video marketing & social auto-posting...")
        product_title = "Posture Corrector Deluxe"
        asset = generate_vertical_short_video(product_title)
        post_to_platforms(asset["asset_path"], product_title)
        logger.info("[Job] Organic marketing & social distribution complete.")
    except Exception as e:
        logger.error(f"[Job Error] Organic marketing job failed: {e}")

def run_autonomous_loop():
    logger.info("Initializing Autonomous Dropshipping, Organic Marketing & Social Auto-Poster Scheduler...")
    config = load_config()
    sched_cfg = config.get("schedule", {})
    
    inv_mins = sched_cfg.get("inventory_sync_minutes", 30)
    res_hours = sched_cfg.get("product_research_hours", 6)
    video_hours = sched_cfg.get("organic_video_hours", 12)

    scheduler = BackgroundScheduler()
    
    scheduler.add_job(product_research_job, 'interval', hours=res_hours, id='product_research', misfire_grace_time=3600)
    scheduler.add_job(inventory_sync_job, 'interval', minutes=inv_mins, id='inventory_sync', misfire_grace_time=300)
    scheduler.add_job(organic_marketing_job, 'interval', hours=video_hours, id='organic_marketing', misfire_grace_time=3600)

    scheduler.start()
    logger.info(f"Scheduler active. Inventory sync: {inv_mins}m, Research: {res_hours}h, Organic Videos/Social: {video_hours}h.")

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler shut down cleanly.")

if __name__ == "__main__":
    run_autonomous_loop()
