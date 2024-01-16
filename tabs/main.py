from tabs.disk import init_disk
from tabs.home import init_home
from tabs.cpu import init_cpu
from tabs.memory import init_memory
from tabs.nework import init_network
from tabs.history import init_history

screenshot_path = "screenshots"

TABS = {
    "home": {
        "button": None,
        "frame": None,
        "init": init_home,
        "image": "home_light.png"
    },
    "cpu": {
        "button": None,
        "frame": None,
        "init": init_cpu,
        "image": "cpu.png"
    },
    "memory": {
        "button": None,
        "frame": None,
        "init": init_memory,
        "image": "memory.png"
    },
    "disk": {
        "button": None,
        "frame": None,
        "init": init_disk,
        "image": "disk.png"
    },
    "network": {
        "button": None,
        "frame": None,
        "init": init_network,
        "image": "network.png"
    },
    "history": {
        "button": None,
        "frame": None,
        "init": init_history,
        "image": "logo.png"
    }
}
