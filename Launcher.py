import platform
import subprocess
import sys
import shutil
import os

def is_python_installed():
    """Check if Python is available."""
    return shutil.which("python3") is not None or shutil.which("python") is not None

def install_python():
    """Advise manual installation of Python."""
    os_type = platform.system()
    if os_type == "Windows":
        print("⚠️ Python not detected. Please install it from https://www.python.org/downloads/windows/")
    elif os_type == "Linux":
        print("⚠️ Python not detected. Attempting install...")
        subprocess.call(["sudo", "apt", "update"])
        subprocess.call(["sudo", "apt", "install", "-y", "python3", "python3-pip"])
    elif os_type == "Darwin":
        print("⚠️ Python not detected. Attempting install...")
        subprocess.call(["brew", "install", "python3"])
    else:
        print("❌ Unsupported OS for Python install.")
        sys.exit(1)

def run_install_tools():
    """Run Install_tools.py if available."""
    if os.path.exists("Install_tools.py"):
        print("🚀 Running Install_tools.py...")
        subprocess.call([sys.executable, "Install_tools.py"])
    else:
        print("⚠️ Install_tools.py not found. Skipping tool installation.")

def main():
    print("==== Digital Forensics Launcher ====\n")

    # 1. Check for Python
    if not is_python_installed():
        install_python()

    # 2. Install necessary tools
    run_install_tools()

    # 3. Detect OS and launch correct forensic tool
    current_os = platform.system()
    if current_os == "Windows":
        print("🔍 Detected Windows. Running Batch Forensics Tool...")
        if os.path.exists("forensic_tools.bat"):
            subprocess.call(["cmd.exe", "/c", "forensic_tools.bat"])
        else:
            print("❌ forensic_tools.bat not found.")
    elif current_os in ["Linux", "Darwin"]:
        print("🔍 Detected Unix-based OS. Running Bash Forensics Tool...")
        if os.path.exists("forensic_tools.sh"):
            subprocess.call(["chmod", "+x", "forensic_tools.sh"])
            subprocess.call(["bash", "forensic_tools.sh"])
        else:
            print("❌ forensic_tools.sh not found.")
    else:
        print("❌ Unsupported OS.")
        sys.exit(1)
    # 4. Run import_platform.py (setup or initialization, if needed)
    if os.path.exists("import_platform.py"):
        print("📦 Running import_platform.py...")
        subprocess.call([sys.executable, "import_platform.py"])
    else:
        print("⚠️ import_platform.py not found.")
print("\n✅ Forensics operations initiated successfully!")
if __name__ == "__main__":
    main()
