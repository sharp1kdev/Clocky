import threading
from datetime import datetime

from GrandBot import BOT, LOGS
from GrandBot import __copystring__, __version__
from GrandBot.helpers import time_has_changed, convert_time_to_string, get_photos_id_list

LOGS.info("Starting avatar changer...")
BOT.start()
ME = BOT.get_me().username
LOGS.info(__copystring__)
LOGS.info(f"You're logged in as \"{ME}\"!")
LOGS.info(f"Your GrandBot is Version {__version__}\n")


def change_picture(time_val):
    threading.Timer(1, change_picture, [convert_time_to_string(datetime.now()), ]).start()
    if time_has_changed(time_val):
        prev_time = convert_time_to_string(datetime.now())
        my = BOT.get_profile_photos("me")
        f_list = get_photos_id_list(my)
        BOT.delete_profile_photos(f_list)
        BOT.set_profile_photo(f"time_images/{prev_time.replace(':', '_')}.jpg")
        LOGS.info(f"Setting current profile pic to {prev_time}.jpg")


change_picture("")
