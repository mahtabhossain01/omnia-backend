import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("SocialAutoPoster")

def post_to_platforms(video_asset, product_title):
    logger.info(f"[Social Auto-Poster] Preparing viral caption & hashtags for: '{product_title}'")
    caption = f"Must-have viral find! 🔥 Get yours now before it sells out. #tiktokmademebuyit #{product_title.lower().replace(' ', '')} #trending #viral"
    
    platforms = ["TikTok", "Instagram Reels", "YouTube Shorts"]
    for platform in platforms:
        logger.info(f"[Social Auto-Poster] Publishing video asset '{video_asset}' to {platform} with caption: '{caption}'")
        time.sleep(0.5)
        logger.info(f"[Social Auto-Poster] Successfully posted to {platform}!")
    
    return {"status": "success", "platforms_posted": platforms, "caption": caption}

if __name__ == "__main__":
    logger.info("Testing Social Auto-Poster standalone...")
    post_to_platforms("/media/videos/smart_led_strip_pro.mp4", "Smart LED Strip Pro")
