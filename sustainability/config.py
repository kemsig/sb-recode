import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Discord and MongoDB settings
DISCORD_BOT_SECRET = os.getenv("DISCORD_BOT_SECRET")
NO_MONGO = bool(os.getenv("NO_MONGO", "false"))
LOCAL_DB_NAME = os.getenv("LOCAL_DB_NAME", 'local.db')


# Bot settings
GACHA_MIN_BALANCE = int(os.getenv("GACHA_MIN_BALANCE", "14"))
ADMIN_CHANNEL_NAME = os.getenv("ADMIN_CHANNEL_NAME", "sustain-admin")
LOG_CHANNEL_NAME = os.getenv("LOG_CHANNEL_NAME", "logs-sustainability")
ROLE_NAME = os.getenv("ROLE_NAME", "Sustain Mod")

MAX_DB_SIZE = int(os.getenv("MAX_DB_SIZE", str(5 * 1024 * 1024)))

# other
SETUP_MESSAGE = f"""# __**:loudspeaker: HOW TO USE THE SUSTAINABILITY BOT**__


## :seedling: STEP-BY-STEP GUIDE

**:white_check_mark: 1. Click *"Claim Your Points"* below to submit a request**  
**:camera_with_flash: 2. Post a photo of you doing something sustainable**  
**:green_circle: 3. Press *Confirm*! A moderator will review your submission and award points**


## :bulb: ADDITIONAL COMMANDS

**:small_blue_diamond: `/points`** — Check how many sustainability points you have  
**:gift: `/gacha`** — Use this if you have **{GACHA_MIN_BALANCE} or more points** to roll for a prize


__:recycle: Stay eco-friendly and keep earning rewards!__

"""

CLAIM_POINTS_MESSAGE = """# :camera_with_flash: Submit Your Sustainability Proof!

Please upload a **photo of your sustainable action** (e.g., recycling, using a reusable bottle, biking, etc.) in the prompt below.

:outbox_tray: Once your image has been successfully submitted:
:white_check_mark: **Press Submit** to send your request to the moderators for review  
:x: **Or press Deny** if you want to cancel the request

A moderator will verify your submission and award your points shortly. Thanks for helping the planet! :earth_africa::seedling:
"""