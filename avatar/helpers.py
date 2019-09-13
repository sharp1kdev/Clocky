from datetime import datetime

from cv2 import putText, FONT_HERSHEY_SIMPLEX, LINE_AA
from numpy import zeros


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
