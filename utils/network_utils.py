import subprocess
import re


def get_connections_network_info():
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("Failed to run command")

    # Parse the output
    lines = result.stdout.split('\n')
    interface_info = {}
    for line in lines:
        # Using regular expression to match key-value pairs
        match = re.match(r'\s*(.+?)\s*:\s*(.+)', line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            interface_info[key] = value

    return interface_info
