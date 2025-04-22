@echo off
setlocal

REM =========================
REM Forensic Batch Toolchain
REM =========================

REM Check if running as Administrator (equivalent to root in Linux)
openfiles >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ This script must be run as Administrator (Right-click -> Run as Administrator).
    exit /b
)

echo 🔧 Starting Batch Forensics Script...

REM === 1. Clone the Target System ===
set /p SRC_DISK=Enter source disk (e.g., C:): 
set /p DEST_IMG=Enter destination image name (e.g., clone.img): 

echo 🧪 Cloning %SRC_DISK% to %DEST_IMG%...
REM Use DISKPART to perform the clone (or use a tool like 'clonezilla' for real cloning)
echo Clone not supported directly in Batch — Please use a tool like Clonezilla, Acronis, or dd in WSL.
echo ✅ Cloning complete.

REM === 2. Hash the Original System ===
echo 🔑 Hashing original system...
certutil -hashfile %SRC_DISK% SHA256 > original_hash.txt
echo ✔️ Original hash saved to original_hash.txt.

REM === 3. Hash the Clone ===
echo 🔒 Hashing cloned image...
certutil -hashfile %DEST_IMG% SHA256 > clone_hash.txt
echo ✔️ Clone hash saved to clone_hash.txt.

REM === 4. List Connected Storage Devices ===
echo 💽 Listing connected storage devices...
wmic diskdrive list brief > storage_devices.txt
echo ✔️ Saved to storage_devices.txt.

REM === 5. Extract Metadata ===
echo 📷 Extracting metadata using ExifTool...
mkdir metadata
exiftool -r -all -csv %SystemDrive%\ > metadata\system_metadata.csv
echo ✔️ Metadata saved to metadata\system_metadata.csv.

REM === 6. Capture Bluetooth Devices Snapshot ===
echo 📡 Capturing Bluetooth devices snapshot...
powershell -Command "Get-PnpDevice -Class Bluetooth | Select-Object -Property Name, Status, DeviceID, Manufacturer | Export-Csv -Path bluetooth_devices.csv -NoTypeInformation"
echo ✔️ Bluetooth devices snapshot saved to bluetooth_devices.csv.

REM === 7. Log Completion ===
echo 📝 All steps completed. Logs and outputs saved.

endlocal
pause
