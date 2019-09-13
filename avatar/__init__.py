import logging
import os
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path
from numpy import zeros
from cv2 import putText, imwrite, LINE_AA, FONT_HERSHEY_SIMPLEX

from pyrogram import Client

# We need logging this early for our Version Check
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.INFO)
LOGS = logging.getLogger(__name__)

# Check for Python 3.6 or newer
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGS.error("You MUST use at least Python 3.6. Bot Quitting")
    quit(1)

# Now for the rest
__version__ = '0.0.1'
__author__ = 'theGrand'
__source__ = 'https://github.com/sharp1kdev/avabot'
__copyright__ = 'Copyright (c) 2019 ' + __author__

__copystring__ = f"AvaBot v{__version__} | {__copyright__}"

LOGGER = os.getenv("LOGGER")
try:
    LOGGER_GROUP = int(0)
except ValueError:
    LOGGER_GROUP = 0

# Create Database if there is none yet.
AVA_DB = str(Path(__file__).parent.parent / 'avabot.db')
IMAGES_DIR = Path(__file__).parent.parent / 'time_images'

LOGS.info("Checking Database...")
db = sqlite3.connect(AVA_DB)
c = db.cursor()
c.executescript(
    "CREATE TABLE IF NOT EXISTS welcome "
    "(chat_id INT UNIQUE ON CONFLICT FAIL, greet TEXT, chat_title TEXT);")
db.commit()
db.close()
LOGS.info("Check done.")

LOGS.info("Checking Files...")

start_time = datetime.strptime("2019-01-01", "%Y-%m-%d")
end_time = start_time + timedelta(days=1)


def convert_time_to_string(dt):
    return f"{dt.hour:02}:{dt.minute:02}"


def get_black_background():
    return zeros((500, 500))


def generate_image_with_text(text):

    image = get_black_background()

    putText(image, text, (int(image.shape[0] * 0.05), int(image.shape[1] * 0.6)), FONT_HERSHEY_SIMPLEX, 5,
            (255, 255, 0), 5, LINE_AA)

    return image


def time_has_changed(prev_time):
    return convert_time_to_string(datetime.now()) != prev_time


def get_photos_id_list(photos):
    list_files = list()
    for item in photos:
        file_id = item.file_id
        list_files.append(str(file_id))

    return list_files


if not IMAGES_DIR.exists():
    IMAGES_DIR.mkdir()

if os.listdir(IMAGES_DIR).__len__() <= 0:
    while start_time < end_time:
        text = convert_time_to_string(start_time)
        safe_text = text.replace(':', '_')
        file_name = f"{safe_text}.jpg"
        image = generate_image_with_text(text)
        imwrite("%s/%s.jpg" % (IMAGES_DIR, safe_text), image)
        start_time += timedelta(minutes=1)
        LOGS.info(f"Generating {file_name}")

LOGS.info("File check Done!")

# Prepare the bot
BOT = Client(
    session_name="AvaBot",
    api_id=os.getenv("TELEGRAM_APP_ID"),
    api_hash=os.getenv("TELEGRAM_APP_HASH"),
    app_version=f"AvaBot \U0001f525\U0001F916 v{__version__}")

# Global Variables
ISAFK = False
AFK_REASON = "No Reason"
START_TIME = datetime.now()
