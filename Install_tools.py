import shutil
import subprocess
import platform
import os

def is_tool_installed(tool_name):
    """Check if a tool exists on PATH."""
    return shutil.which(tool_name) is not None

def install_tool_linux(tool_name):
    """Install a tool on Linux using apt."""
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        
        # Special case: exiftool needs the correct apt package
        if tool_name == "exiftool":
            apt_package = "libimage-exiftool-perl"
        else:
            apt_package = tool_name

        subprocess.run(["sudo", "apt-get", "install", "-y", apt_package], check=True)
        print(f"✅ {tool_name} installed successfully (Linux).")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {tool_name} on Linux.")

def install_tool_mac(tool_name):
    """Install a tool on MacOS using brew."""
    try:
        subprocess.run(["brew", "install", tool_name], check=True)
        print(f"✅ {tool_name} installed successfully (macOS).")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {tool_name} on macOS.")

def install_tool_windows(tool_name):
    """Advise user to install manually on Windows."""
    print(f"⚠️ Please manually install {tool_name} on Windows.")
    print(f"Visit: https://chocolatey.org/packages/{tool_name} (if you have Chocolatey)")
    print(f"Or search manually for an installer.")

def install_tool(tool_name):
    """Check OS and install the tool accordingly."""
    if is_tool_installed(tool_name):
        print(f"✅ {tool_name} is already installed.")
        return

    print(f"🔎 {tool_name} not found. Attempting installation...")

    os_type = platform.system()

    if os_type == "Linux":
        install_tool_linux(tool_name)
    elif os_type == "Darwin":
        install_tool_mac(tool_name)
    elif os_type == "Windows":
        install_tool_windows(tool_name)
    else:
        print(f"Unsupported OS: {os_type}")

def main():
    tools = ["exiftool", "tree"]

    print("==== Tool Installer ====")
    for tool in tools:
        install_tool(tool)

    print("\n✅ All tool checks complete.")

if __name__ == "__main__":
    main()
