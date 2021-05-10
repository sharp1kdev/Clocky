import threading
from datetime import datetime

from GrandBot import BOT, LOGS
from GrandBot.helpers import time_has_changed, convert_time_to_string, generate_doge_image, get_coin_data_text

LOGS.info("Starting avatar changer...")
try:
    BOT.start()
except Exception as e:
    print(e)


def change_picture(time_val):
    threading.Timer(1, change_picture, [convert_time_to_string(datetime.now()), ]).start()
    if time_has_changed(time_val):
        prev_time = convert_time_to_string(datetime.now())
        text = get_coin_data_text()
        generate_doge_image(text)
        # BOT.set_profile_photo(f"time_images/{prev_time.replace(':', '_')}.jpg")
        BOT.set_profile_photo("doge.jpg")
        my_photos = iter(BOT.iter_profile_photos("me", offset=1))
        for image in my_photos:
            BOT.delete_profile_photos(image.file_id)
        LOGS.info("Setting current avatar to {}.jpg".format(prev_time))


change_picture("")
