import platform
import subprocess
import os
import sys

def main():
    current_os = platform.system()
    if current_os == "Windows":
        print("🔍 Detected Windows. Running Batch Forensics Tool...")
        subprocess.call(["forensic_tools.bat"], shell=True)
    elif current_os == "Linux" or current_os == "Darwin":
        print("🔍 Detected Unix-based OS. Running Bash Forensics Tool...")
        subprocess.call(["bash" ,"sudo", "chmod", "+x", "forensic_tools.sh"])
        subprocess.call(["bash", "./forensic_tools.sh"])
    else:
        print("❌ Unsupported OS.")
        sys.exit(1)

if __name__ == "__main__":
    main()
