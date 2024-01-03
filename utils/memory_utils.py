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
