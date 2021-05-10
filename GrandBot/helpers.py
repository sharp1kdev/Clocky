from datetime import datetime
import requests
from cv2 import putText, imwrite, FONT_HERSHEY_SIMPLEX, LINE_AA
from numpy import zeros


def convert_time_to_string(dt):
    return f"{dt.hour:02}:{dt.minute:02}"


def get_black_background():
    return zeros((500, 500))


def generate_doge_image(text):
    y0, dy = 60, 100
    image = zeros((500, 500))
    x = 10

    for i, line in enumerate(text.split('\n')):
        y = y0 + i * dy
        putText(image, line, (x, y), 2, 2, (255, 255, 0), 3, 5)
    imwrite('doge.jpg', image)


def get_coin_data_text():
    json_data = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=usd%2Cuah%2Crub')
    doge_info = json_data.json()['dogecoin']
    usd = doge_info['usd']
    uah = doge_info['uah']
    rub = doge_info['rub']

    current_time = datetime.now().time().__str__()
    current_time = current_time.split(':')
    formatted_time = "{}:{}".format(current_time[0], current_time[1])
    text = "   DOGECOIN\n    {}\nUSD: {}\nUAH: {}\nRUB: {}".format(formatted_time, usd, uah, rub)
    return text


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
