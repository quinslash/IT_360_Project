import platform
import subprocess
import os
import sys

def main():
    current_os = platform.system()
    if current_os == "Windows":
        print("🔍 Detected Windows. Running Batch Forensics Tool...")
        subprocess.run(["forensic_tools.bat"], shell=True)
    elif current_os == "Linux" or current_os == "Darwin":
        print("🔍 Detected Unix-based OS. Running Bash Forensics Tool...")
        subprocess.run(["chmod", "+x", "forensic_tools.bash"])
        subprocess.run(["./forensic_tools.bash"])
    else:
        print("❌ Unsupported OS.")
        sys.exit(1)

if __name__ == "__main__":
    main()
