import os
from dotenv import load_dotenv
from loguru import logger

def load_config() -> tuple[str, str]:
    """Load configuration from environment variables."""
    load_dotenv()
    
    app_key = os.getenv("APP_KEY")
    app_secret = os.getenv("APP_SECRET")

    if not app_key or not app_secret:
        logger.error("App key or secret is missing.")
        raise ValueError("App key or secret is missing.")

    return app_key, app_secret
