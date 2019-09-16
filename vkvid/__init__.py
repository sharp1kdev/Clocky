import logging
import os
import sqlite3
import sys
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path


from pyrogram import Client

# We need logging this early for our Version Check
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.INFO)
LOGS = logging.getLogger(__name__)

ENVFILE = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=ENVFILE)

# Check for Python 3.6 or newer
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGS.error("You MUST use at least Python 3.6. Bot Quitting")
    quit(1)

# Now for the rest
__version__ = '0.0.1'
__author__ = 'theGrand'
__source__ = 'https://github.com/sharp1kdev/TelegramBot'
__copyright__ = 'Copyright (c) 2019 ' + __author__

__copystring__ = f"AvaBot v{__version__} | {__copyright__}"

LOGGER = os.getenv("LOGGER")
try:
    LOGGER_GROUP = int(0)
except ValueError:
    LOGGER_GROUP = 0

# Create Database if there is none yet.
AVA_DB = str(Path(__file__).parent.parent / 'vkbot.db')

LOGS.info("Checking Database...")
db = sqlite3.connect(AVA_DB)
c = db.cursor()
c.executescript(
    "CREATE TABLE IF NOT EXISTS welcome "
    "(chat_id INT UNIQUE ON CONFLICT FAIL, greet TEXT, chat_title TEXT);")
db.commit()
db.close()
LOGS.info("Check done.")

# Prepare the bot
VKBOT = Client(
    session_name="VK_Anime_Videos",
    api_id=os.getenv("TELEGRAM_APP_ID"),
    api_hash=os.getenv("TELEGRAM_APP_HASH"),
    app_version=f"AvaBot \U0001f525\U0001F916 v{__version__}")

# Global Variables
ISAFK = False
AFK_REASON = "No Reason"
START_TIME = datetime.now()
