import psutil
from cpuinfo import cpuinfo
from utils.general_utils import bytes2human


def get_per_core_usage():
    cpus = {}
    for index, percent in enumerate(list(psutil.cpu_percent(percpu=True))):
        cpus[f"cpu{index + 1}"] = f"{percent}%"
    return cpus


def update_cpu_function():
    return psutil.cpu_percent()


def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    cpu_info = {
        "Brand": info["brand_raw"],
        "Architecture": info["arch"],
        "Bits": info["bits"],
        "Cores": psutil.cpu_count(logical=False),
        "Threads": psutil.cpu_count(logical=True),
        "Frequency": info["hz_actual_friendly"],
        "L2 Cache": bytes2human(int(info["l2_cache_size"])),
        "L3 Cache": bytes2human(int(info["l3_cache_size"])),
        "Vendor": info["vendor_id_raw"],
        # "Family": info["family_raw"],
        # "Model": info["model_raw"],
        "Stepping": info["stepping"],
        "Flags": info["flags"]
    }
    return cpu_info
