import os
import psutil
import shutil
from utils.general_utils import bytes2human


def get_partitions():
    return [part for part in psutil.disk_partitions(all=False) if
            not (os.name == 'nt' and ('cdrom' in part.opts or part.fstype == ''))]


def get_partition_info(part):
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


def get_partition_usage(part: psutil._common.sdiskpart):
    return shutil.disk_usage(part.mountpoint)
