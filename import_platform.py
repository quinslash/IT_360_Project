import platform
import os
import psutil
import subprocess
from datetime import datetime
import getpass
import logging

# Setup logging
logging.basicConfig(filename="forensics.log", level=logging.INFO, format="%(asctime)s: %(message)s")

# === 1. SYSTEM & DEVICE INFO ===

def get_windows_drives():
    if platform.system() == "Windows":
        partitions = psutil.disk_partitions()
        print("Available Windows Drives:")
        for partition in partitions:
            print(f"Drive: {partition.device}, Type: {partition.fstype}")
    else:
        print("Not a Windows filesystem")

def get_unix_drives():
    if platform.system() in ["Linux", "Darwin"]:
        partitions = psutil.disk_partitions()
        print("Available Unix Drives:")
        for partition in partitions:
            print(f"Mount Point: {partition.mountpoint}, Device: {partition.device}, Type: {partition.fstype}")
    else:
        print("Not a Unix filesystem")

def get_system_info():
    system_info = {
        "OS": platform.system(),
        "OS_Version": platform.version(),
        "OS_Release": platform.release(),
        "Architecture": platform.architecture()[0],
        "Processor": platform.processor(),
        "Machine_Type": platform.machine(),
        "Hostname": platform.node()
    }
    return system_info

def print_system_info():
    info = get_system_info()
    print("System Information:")
    for key, value in info.items():
        print(f"{key}: {value}")
    print()
    logging.info("System information collected.")

# === 2. TOOL DEPLOYMENT ===

def deploy_tool():
    print("Deploying necessary tools...")
    if platform.system() == "Linux":
        os.system('sudo apt update && sudo apt install -y exiftool tree')
        print("Tools deployed (Linux).")
    elif platform.system() == "Darwin":
        os.system('brew install exiftool tree')
        print("Tools deployed (macOS).")
    else:
        print("Tool deployment not supported on this OS.")
    logging.info("Tool deployment attempted.")

# === 3. FILESYSTEM MAP HANDLING ===

def store_filesystem_map():
    try:
        os.makedirs("output", exist_ok=True)
        os.rename("filesystem_map.txt", "output/filesystem_map_readable.txt")
        print("Filesystem map stored.")
        logging.info("Filesystem map stored in output directory.")
    except Exception as e:
        print(f"Error moving filesystem map: {e}")
        logging.error(f"Failed to move filesystem map: {e}")

# === 4. HASH COMPARISON ===

def compare_hashes():
    try:
        with open('original_hash.txt') as f1, open('clone_hash.txt') as f2:
            hash1 = f1.read().split()[0]
            hash2 = f2.read().split()[0]
            if hash1 == hash2:
                print("Hash integrity check passed ✅")
                logging.info("Hash integrity check passed.")
            else:
                print("WARNING: Hash mismatch detected ❌")
                logging.warning("Hash mismatch detected.")
    except FileNotFoundError as e:
        print(f"Hash file missing: {e}")
        logging.error(f"Hash file missing: {e}")

# === 5. CHAIN OF CUSTODY LOGGING ===

def log_chain_of_custody():
    user = getpass.getuser()
    timestamp = datetime.now().isoformat()
    log_entry = f"Clone created by {user} at {timestamp}"
    with open("chain_of_custody.log", "a") as log:
        log.write(log_entry + "\n")
    print("Chain of custody logged.")
    logging.info("Chain of custody recorded.")

# === 6. OS DETECTION ===

def detect_os():
    os_info = platform.system()
    print(f"Detected OS: {os_info}")
    logging.info(f"OS Detected: {os_info}")
    return os_info

# === 7. MAIN DRIVER FUNCTION ===

def main():
    print("==== Digital Forensics Tool ====\n")

    print_system_info()

    os_type = detect_os()
    print()

    get_unix_drives()
    get_windows_drives()
    print()

    deploy_tool()
    print()

    store_filesystem_map()
    print()

    compare_hashes()
    print()

    log_chain_of_custody()
    print("\n✅ All forensic operations completed)
