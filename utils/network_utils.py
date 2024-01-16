import subprocess
import re
import psutil
import time


def get_devices_info():
    info = psutil.net_if_stats()
    keys_to_delete = []
    for key, value in info.items():
        if isinstance(value, tuple):
            if not value.isup:
                keys_to_delete.append(key)
            else:
                info[key] = value._asdict()
    for key in keys_to_delete:
        del info[key]
    return info


def get_connections_network_info():
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("Failed to run command")

    lines = result.stdout.split('\n')
    interface_info = {}
    for line in lines:
        match = re.match(r'\s*(.+?)\s*:\s*(.+)', line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            interface_info[key] = value
    return interface_info


def update_download_speed():
    initial_data = psutil.net_io_counters()
    interval = 1
    time.sleep(interval)
    final_data = psutil.net_io_counters()

    return (final_data.bytes_recv - initial_data.bytes_recv) / interval


def update_upload_speed():
    initial_data = psutil.net_io_counters()
    interval = 1
    time.sleep(interval)
    final_data = psutil.net_io_counters()

    return (final_data.bytes_sent - initial_data.bytes_sent) / interval
