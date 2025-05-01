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
    for partition in psutil.disk_partitions():
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
        if not os.path.exists("filesystem_map.txt"):
            print("⚠️ filesystem_map.txt not found. creating")
            logging.warning("filesystem_map.txt not found. One created")
            subprocess.call(["sudo", "touch", "filesystem_map.txt"])
            return
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
        result = subprocess.run([
            "exiftool", "-r", "-json", target_dir
        ], capture_output=True, text=True, check=True)
        forensic_data["ExifMetadata"] = json.loads(result.stdout)
        logging.info(f"Metadata collected from {target_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error running exiftool: {e}")
        logging.error(f"Exiftool failed: {e}")

# === 7. FINAL XML OUTPUT ===
CHUNK_SIZE_MB = 24
CHUNK_SIZE_BYTES = CHUNK_SIZE_MB * 1024 * 1024

def save_forensic_report(output_file):
    output_file_base = os.path.splitext(output_file)[0]
    root = ET.Element("ForensicReport")

    sysinfo = ET.SubElement(root, "SystemInfo")
    for key, value in forensic_data["SystemInfo"].items():
        ET.SubElement(sysinfo, key).text = str(value)

    drives = ET.SubElement(root, "Drives")
    for drive in forensic_data["Drives"]:
        d = ET.SubElement(drives, "Drive")
        for key, value in drive.items():
            ET.SubElement(d, key).text = str(value)

    hash_check = ET.SubElement(root, "HashIntegrity")
    hash_check.text = forensic_data["HashCheck"]

    chain = ET.SubElement(root, "ChainOfCustody")
    chain.text = forensic_data["ChainOfCustody"]

    storage = ET.SubElement(root, "StorageDevices")
    for device in forensic_data.get("StorageDevices", []):
        ET.SubElement(storage, "Device").text = device

    csvmeta = ET.SubElement(root, "CSV_Metadata")
    for entry in forensic_data.get("CSV_Metadata", []):
        file_elem = ET.SubElement(csvmeta, "File")
        for key, value in entry.items():
            ET.SubElement(file_elem, key.replace(" ", "_")).text = str(value)

    metadata = ET.SubElement(root, "ExifMetadata")
    for file_info in forensic_data["ExifMetadata"]:
        file_elem = ET.SubElement(metadata, "File")
        for key, value in file_info.items():
            key_clean = key.replace(" ", "_")
            ET.SubElement(file_elem, key_clean).text = str(value)

    base_output = f"{output_file_base}_base.xml"
    ET.ElementTree(root).write(base_output, encoding="utf-8", xml_declaration=True)
    print(f"✅ Base forensic report saved as {base_output}")

    csv_metadata = forensic_data.get("CSV_Metadata", [])
    chunk_root = ET.Element("CSV_Metadata")
    part_num = 1
    size_estimate = 0

    for entry in csv_metadata:
        file_elem = ET.SubElement(chunk_root, "File")
        for key, value in entry.items():
            tag = key.replace(" ", "_")
            ET.SubElement(file_elem, tag).text = str(value)

        size_estimate = len(ET.tostring(chunk_root, encoding="utf-8"))

        if size_estimate >= CHUNK_SIZE_BYTES:
            chunk_file = f"{output_file_base}_part{part_num}.xml"
            ET.ElementTree(chunk_root).write(chunk_file, encoding="utf-8", xml_declaration=True)
            print(f"✅ CSV metadata chunk saved as {chunk_file}")
            part_num += 1
            chunk_root = ET.Element("CSV_Metadata")
            size_estimate = 0

    if len(chunk_root):
        chunk_file = f"{output_file_base}_part{part_num}.xml"
        ET.ElementTree(chunk_root).write(chunk_file, encoding="utf-8", xml_declaration=True)
        print(f"✅ Final CSV metadata chunk saved as {chunk_file}")

# === 8. FILE LOADERS ===
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
            csv_metadata = [row for row in reader]
            forensic_data["CSV_Metadata"] = csv_metadata
            logging.info("CSV metadata loaded.")
    except FileNotFoundError:
        forensic_data["CSV_Metadata"] = []
        logging.warning("system_metadata.csv not found.")

# === 9. MAIN DRIVER ===
def main():
    print("==== Digital Forensics Tool ====\n")
    get_system_info()
    get_drives()
    deploy_tool()
    store_filesystem_map()
    compare_hashes()
    log_chain_of_custody()
    run_exiftool("/home/username")  # UPDATE THIS PATH
    load_storage_devices()
    load_metadata_csv()
    save_forensic_report("forensics_report.xml")

if __name__ == "__main__":
    main()
