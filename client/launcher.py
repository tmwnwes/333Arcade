import subprocess
import os
import platform
from pathlib import Path

def launch_app(path):
    full_path = Path(path).absolute()
    ext = full_path.suffix.lower()
    os_name = platform.system()

    # macOS .app bundle
    if ext == ".app" and os_name == "Darwin":
        subprocess.Popen(["open", str(full_path)])
        return

    # Windows or mac shell scripts
    if ext in [".bat", ".cmd", ".sh"]:
        subprocess.Popen(str(full_path), shell=True, cwd=str(full_path.parent))
        return

    # Normal executables (.exe or unix binaries)
    if full_path.is_file():
        subprocess.Popen([str(full_path)], cwd=str(full_path.parent))
    else:
        print("Executable not found:", full_path)
