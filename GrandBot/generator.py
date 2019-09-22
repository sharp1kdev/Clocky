from datetime import datetime, timedelta
from pathlib import Path
from cv2 import imwrite
from GrandBot.helpers import generate_image_with_text, convert_time_to_string


def try_init_folders():

    # set start and end time
    start_time = datetime.strptime("2019-01-01", "%Y-%m-%d")
    end_time = start_time + timedelta(days=1)

    # fill folder with images
    dir_path = Path("time_images")
    if not dir_path.exists():
        dir_path.mkdir()

    while start_time < end_time:
        text = convert_time_to_string(start_time)
        safe_text = text.replace(':', '_')
        file_name = f"{safe_text}.jpg"
        image = generate_image_with_text(text)
        imwrite("%s/%s.jpg" % (dir_path, safe_text), image)
        start_time += timedelta(minutes=1)
        print(f"Generating {file_name}")


try_init_folders()
