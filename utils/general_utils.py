import os
import re
from datetime import datetime


def string_to_float(string):
    """
    Converts a string to a float.
    :param string: string to convert
    :return:
    """
    return float(re.sub(r'[a-zA-Z%]', '', string))


def bytes2human(n, format="%(value).1f%(symbol)s"):
    """
    Converts bytes to human readable format.
    :param n: the number of bytes
    :param format: the format of the output
    :return:
    """
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
    """
    Converts a speed in bytes to a human readable format.
    :param n:
    :return:
    """
    return f'{bytes2human(n)}/s'


def seconds2human(seconds):
    """
    Converts seconds to a human readable format.
    :param seconds: number of seconds
    :return:
    """
    h = seconds / 3600
    if h >= 1:
        return f"{round(h, 1)} h"
    m = seconds / 60
    if m >= 1:
        return f"{round(m, 1)} m"
    return f"{round(seconds, 1)} s"


def choose_equidistant_timestamps(length, max_count):
    """
    Chooses timestamps that are equidistant. to show on a chart.
    :param length: the lenght of the data set
    :param max_count: maximum number of timestamps
    :return: the major timestamps of a list
    """
    return [(max(length, max_count) // max_count + 1) * i for i in range(max_count)]


def get_current_date_time():
    """
    Gets the current date and time as a string.
    :return: current date as a string
    """
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def create_directory_if_not_exists(path):
    """
    Creates a directory if it doesn't exist.
    :param path: the path of the directory
    :return: void
    """
    if not os.path.exists(path):
        os.makedirs(path)
