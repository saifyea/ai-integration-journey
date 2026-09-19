# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# App Settings
APP_NAME = "AI Customer Service Bot"
APP_VERSION = "1.0.0"
MAX_TOKENS = 500
MODEL = "claude-haiku-4-5-20251001"

# Business Info
BUSINESS_NAME = "Saif's Kids Store"
BUSINESS_CONTACT = "Facebook: Saif's Kids Store"

# Products
PRODUCTS = {
    "bangladesh map puzzle": {
        "price": 450,
        "age": "৫-১২ বছর",
        "stock": True
    },
    "magic drawing board": {
        "price": 350,
        "age": "৩-১০ বছর",
        "stock": True
    },
    "flash cards": {
        "price": 250,
        "age": "৩-৬ বছর",
        "stock": True
    }
}