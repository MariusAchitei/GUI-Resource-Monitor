import subprocess

import psutil

from utils.general_utils import bytes2human

memory_type_by_code = {
    "0": "Unknown",
    "1": "Other",
    "2": "DRAM",
    "3": "Synchronous DRAM",
    "4": "Cache DRAM",
    "5": "EDO",
    "6": "EDRAM",
    "7": "VRAM",
    "8": "SRAM",
    "9": "RAM",
    "10": "ROM",
    "11": "Flash",
    "12": "EEPROM",
    "13": "FEPROM",
    "14": "EPROM",
    "15": "CDRAM",
    "16": "3DRAM",
    "17": "SDRAM",
    "18": "SGRAM",
    "19": "RDRAM",
    "20": "DDR",
    "21": "DDR2",
    "22": "DDR2 FB-DIMM",
    "23": "Reserved",
    "24": "DDR3",
    "25": "FBD2",
    "26": "DDR4"
}


def get_memory_type_by_code(code):
    return memory_type_by_code[code]


def memory_precent_update_function():
    return psutil.virtual_memory().percent


def memory_bytes_update_function():
    return psutil.virtual_memory().used


def get_memory_limit():
    return 0, psutil.virtual_memory().total


def get_ram_info():
    cmd = "wmic MemoryChip get /format:csv"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result, error = process.communicate()
    print(result)
    data = []
    lines = [line for line in result.split("\n") if line != ""]
    key_line = lines[0]
    keys = [key for key in key_line.split(",")]
    value_lines = [line for (index, line) in enumerate(lines) if index > 0 and line != ""]
    for index, line in enumerate(value_lines):
        slot = {}
        values = [value for value in line.split(",")]
        for i in range(0, len(values)):
            slot[keys[i]] = values[i]
        slot["Capacity"] = bytes2human(int(slot["Capacity"]))
        slot["ConfiguredClockSpeed"] = f"{slot['ConfiguredClockSpeed']} MHz"
        slot["Speed"] = f"{slot['Speed']} MHz"
        slot["MemoryType"] = get_memory_type_by_code(slot["MemoryType"])
        data.append(slot)
    if error:
        return error
    return data
