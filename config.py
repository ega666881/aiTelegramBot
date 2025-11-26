import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
COMET_API_URL = os.getenv("COMET_API_URL")
COMET_API_TOKEN = os.getenv("COMET_API_TOKEN")
TOKEN_USD_PRICE = os.getenv("TOKEN_USD_PRICE")
MARGIN = os.getenv("MARGIN")
GROUP_RATIO = os.getenv("GROUP_RATIO")
