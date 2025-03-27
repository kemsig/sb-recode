import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Discord and MongoDB settings
DISCORD_BOT_SECRET = os.getenv("DISCORD_BOT_SECRET")


# Bot settings
GACHA_MIN_BALANCE = int(os.getenv("GACHA_MIN_BALANCE", "14"))
ADMIN_CHANNEL_NAME = os.getenv("ADMIN_CHANNEL_NAME", "sustain-admin")
LOG_CHANNEL_NAME = os.getenv("LOG_CHANNEL_NAME", "logs-sustainability")
ROLE_NAME = os.getenv("ROLE_NAME", "Sustain Mod")

MAX_DB_SIZE = int(os.getenv("MAX_DB_SIZE", str(5 * 1024 * 1024)))