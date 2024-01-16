import os
import re
from datetime import datetime


def string_to_float(string):
    return float(re.sub(r'[a-zA-Z%]', '', string))


def bytes2human(n, format="%(value).1f%(symbol)s"):
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols[1:]):
        prefix[s] = 1 << (i + 1) * 10
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format % locals()
    return format % dict(symbol=symbols[0], value=n)


def speed_bytes2human2(n):
    return f'{bytes2human(n)}/s'


def seconds2human(seconds):
    h = seconds / 3600
    if h >= 1:
        return f"{round(h, 1)} h"
    m = seconds / 60
    if m >= 1:
        return f"{round(m, 1)} m"
    return f"{round(seconds, 1)} s"


def choose_equidistant_timestamps(length, max_count):
    return [(max(length, max_count) // max_count + 1) * i for i in range(max_count)]


def get_current_date_time():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
