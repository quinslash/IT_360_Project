import platform
import os
import psutil
import subprocess
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
import getpass
import logging

# Setup logging
logging.basicConfig(filename="forensics.log", level=logging.INFO, format="%(asctime)s: %(message)s")

# Storage for collected forensic data
forensic_data = {
    "SystemInfo": {},
    "Drives": [],
    "HashCheck": "",
    "ChainOfCustody": "",
    "ExifMetadata": [],
    "StorageDevices": [],
    "CSV_Metadata": []
}

# === 1. SYSTEM & DEVICE INFO ===

def get_system_info():
    info = {
        "OS": platform.system(),
        "OS_Version": platform.version(),
        "OS_Release": platform.release(),
        "Architecture": platform.architecture()[0],
        "Processor": platform.processor(),
        "Machine_Type": platform.machine(),
        "Hostname": platform.node()
    }
    forensic_data["SystemInfo"] = info
    logging.info("System information collected.")

def get_drives():
    drives = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        drive_info = {
            "MountPoint": partition.mountpoint,
            "Device": partition.device,
            "Type": partition.fstype
        }
        drives.append(drive_info)
    forensic_data["Drives"] = drives
    logging.info("Drive information collected.")

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
                forensic_data["HashCheck"] = "Integrity Check Passed"
                print("Hash integrity check passed ✅")
                logging.info("Hash integrity check passed.")
            else:
                forensic_data["HashCheck"] = "Hash Mismatch Detected"
                print("WARNING: Hash mismatch detected ❌")
                logging.warning("Hash mismatch detected.")
    except FileNotFoundError as e:
        forensic_data["HashCheck"] = "Hash files missing"
        print(f"Hash file missing: {e}")
        logging.error(f"Hash file missing: {e}")

# === 5. CHAIN OF CUSTODY LOGGING ===

def log_chain_of_custody():
    user = getpass.getuser()
    timestamp = datetime.now().isoformat()
    entry = f"Clone created by {user} at {timestamp}"
    forensic_data["ChainOfCustody"] = entry
    with open("chain_of_custody.log", "a") as log:
        log.write(entry + "\n")
    print("Chain of custody logged.")
    logging.info("Chain of custody recorded.")

# === 6. METADATA COLLECTION ===

def run_exiftool(target_dir):
    try:
        result = subprocess.run(
            ["exiftool", "-r", "-json", target_dir],
            capture_output=True,
            text=True,
            check=True
        )
        forensic_data["ExifMetadata"] = json.loads(result.stdout)
        logging.info(f"Metadata collected from {target_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error running exiftool: {e}")
        logging.error(f"Exiftool failed: {e}")

# === 7. FINAL XML OUTPUT ===

def save_forensic_report(output_file):
    root = ET.Element("ForensicReport")

    # System Info
    sysinfo = ET.SubElement(root, "SystemInfo")
    for key, value in forensic_data["SystemInfo"].items():
        ET.SubElement(sysinfo, key).text = str(value)

    # Drives
    drives = ET.SubElement(root, "Drives")
    for drive in forensic_data["Drives"]:
        d = ET.SubElement(drives, "Drive")
        for key, value in drive.items():
            ET.SubElement(d, key).text = str(value)

    # Hash Check
    hash_check = ET.SubElement(root, "HashIntegrity")
    hash_check.text = forensic_data["HashCheck"]

    # Chain of Custody
    chain = ET.SubElement(root, "ChainOfCustody")
    chain.text = forensic_data["ChainOfCustody"]
 # Storage Devices
    storage = ET.SubElement(root, "StorageDevices")
    for device in forensic_data.get("StorageDevices", []):
        ET.SubElement(storage, "Device").text = device

    # CSV Metadata
    csvmeta = ET.SubElement(root, "CSV_Metadata")
    for entry in forensic_data.get("CSV_Metadata", []):
        file_elem = ET.SubElement(csvmeta, "File")
        for key, value in entry.items():
            ET.SubElement(file_elem, key.replace(" ", "_")).text = str(value)
    # Metadata
    metadata = ET.SubElement(root, "ExifMetadata")
    for file_info in forensic_data["ExifMetadata"]:
        file_elem = ET.SubElement(metadata, "File")
        for key, value in file_info.items():
            key_clean = key.replace(" ", "_")
            ET.SubElement(file_elem, key_clean).text = str(value)

    # Write XML
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"\n✅ Forensic report saved as {output_file}")

def load_storage_devices():
    try:
        with open('storage_devices.txt', 'r') as file:
            devices = file.read().splitlines()
            forensic_data["StorageDevices"] = devices
            logging.info("Storage devices loaded.")
    except FileNotFoundError:
        forensic_data["StorageDevices"] = []
        logging.warning("storage_devices.txt not found.")

def load_metadata_csv():
    try:
        with open('metadata/system_metadata.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            csv_metadata = []
            for row in reader:
                csv_metadata.append(row)
            forensic_data["CSV_Metadata"] = csv_metadata
            logging.info("CSV metadata loaded.")
    except FileNotFoundError:
        forensic_data["CSV_Metadata"] = []
        logging.warning("system_metadata.csv not found.")

# === 8. MAIN DRIVER FUNCTION ===

def main():
    print("==== Digital Forensics Tool ====\n")

    get_system_info()
    get_drives()
    deploy_tool()
    store_filesystem_map()
    compare_hashes()
    log_chain_of_custody()

    target_dir = "/home/username"  # <- update to safe scan folder
    run_exiftool(target_dir)

    # These must be INSIDE main(), properly indented
    load_storage_devices()
    load_metadata_csv()

    save_forensic_report("forensics_report.xml")

if __name__ == "__main__":
    main()
