import os
import psutil
import shutil
from utils.general_utils import bytes2human


def get_partitions():
    """
    gets the partitions as a list of object.
    :return: data about the partitions.
    """
    return [part for part in psutil.disk_partitions(all=False) if
            not (os.name == 'nt' and ('cdrom' in part.opts or part.fstype == ''))]


def get_partition_info(part):
    """
    Gets info about a partition and maps it to a set standar format.
    :param part: the partition that will be used to get the info.
    :return:
    """
    usage = shutil.disk_usage(part.mountpoint)
    info = {
        "Device": part.device,
        "Total": bytes2human(usage.total),
        "Used": bytes2human(usage.used),
        "Free": bytes2human(usage.free),
        "Use": f'{usage.used * 100 // usage.total}%',
        "Type": part.fstype,
        "Mount": part.mountpoint
    }
    return info


def get_partition_usage(part):
    """
    Gets the usage of a partition.
    :param part: the partition that will be used to get the usage.
    :return:
    """
    return shutil.disk_usage(part.mountpoint)
