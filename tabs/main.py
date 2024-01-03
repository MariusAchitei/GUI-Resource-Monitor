from tabs.disk import init_disk
from tabs.home import init_home
from tabs.cpu import init_cpu
from tabs.memory import init_memory

TABS = {
    "home": {
        "button": None,
        "frame": None,
        "init": init_home
    },
    "cpu": {
        "button": None,
        "frame": None,
        "init": init_cpu
    },
    "memory": {
        "button": None,
        "frame": None,
        "init": init_memory
    },
    "disk": {
        "button": None,
        "frame": None,
        "init": init_disk
    }
}
