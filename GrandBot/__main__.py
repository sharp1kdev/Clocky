import threading
from datetime import datetime

from GrandBot import BOT, LOGS
from GrandBot.helpers import time_has_changed, convert_time_to_string

LOGS.info("Starting avatar changer...")
BOT.start()


def change_picture(time_val):
    threading.Timer(1, change_picture, [convert_time_to_string(datetime.now()), ]).start()
    if time_has_changed(time_val):
        prev_time = convert_time_to_string(datetime.now())
        BOT.set_profile_photo(f"time_images/{prev_time.replace(':', '_')}.jpg")
        my_photos = iter(BOT.iter_profile_photos("me", offset=1))
        for image in my_photos:
            BOT.delete_profile_photos(image.file_id)
        LOGS.info("Setting current avatar to {}.jpg".format(prev_time))


change_picture("")
