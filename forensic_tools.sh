forensic_tools.sh
#!/bin/bash

# ========================
# Forensic Bash Toolchain
# ========================

# Ensure script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root."
   exit 1
fi

echo "🔧 Starting Bash Forensics Script..."

# === 1. Clone the Target System ===
read -p "Enter source disk (e.g., /dev/sda): " SRC_DISK
read -p "Enter destination image name (e.g., clone.img): " DEST_IMG

echo "🧪 Cloning $SRC_DISK to $DEST_IMG..."
dd if="$SRC_DISK" of="$DEST_IMG" bs=4M status=progress
echo "✅ Cloning complete."

# === 2. Hash the Original System ===
echo "🔑 Hashing original system..."
sha256sum "$SRC_DISK" > original_hash.txt
echo "✔️  Original hash saved to original_hash.txt."

# === 3. Hash the Clone ===
echo "🔒 Hashing cloned image..."
sha256sum "$DEST_IMG" > clone_hash.txt
echo "✔️  Clone hash saved to clone_hash.txt."

# === 4. List Connected Storage Devices ===
echo "💽 Listing connected storage devices..."
lsblk > storage_devices.txt
echo "✔️  Saved to storage_devices.txt."

# === 5. Extract Metadata from Root ===
echo "📷 Extracting metadata using exiftool..."
mkdir -p metadata
find / -path /proc -prune -o -path /sys -prune -o -path /dev -prune -o -path /run -prune -o -type f -print | xargs exiftool -csv > metadata/system_metadata.csv
echo "✔️  Metadata saved to metadata/system_metadata.csv."

echo "Launching Python Script" 

# === 6. Log Completion ===
echo "📝 All steps completed. Logs and outputs saved."
