import subprocess
import sys
import shutil
import platform
import os
from pathlib import Path


def parse_launch_version(version: str | None):
    if version is None:
        return None, None
    
    if "=" in version:
        # format: python=C:/path/to/python.exe
        runtime, path = version.split("=", 1)
        return runtime.lower(), path.strip()

    # format: python3.11, java17, etc
    return version.lower(), None


def launch_app(path, launch_version=None):
    full_path = Path(path).absolute()
    ext = full_path.suffix.lower()
    os_name = platform.system()

    if not full_path.exists():
        print("ERROR: Path does not exist:", full_path)
        return

    runtime, custom_path = parse_launch_version(launch_version)

    # detect correct interpreter for .py files
    if ext == ".py":
        if runtime and runtime.startswith("python"):

            # custom absolute interpreter
            if custom_path:
                python_exec = custom_path

            # version-based detection (python3.11 → use that executable)
            else:
                python_exec = shutil.which(runtime) or sys.executable

            print("Launching Python using:", python_exec)
            subprocess.Popen([python_exec, str(full_path)], cwd=str(full_path.parent))
            return

        # fallback
        subprocess.Popen([sys.executable, str(full_path)], cwd=str(full_path.parent))
        return

    # JAR files
    if ext == ".jar":
        java_exec = None

        if runtime and runtime.startswith("java"):
            java_exec = custom_path or shutil.which(runtime)

        if java_exec is None:
            java_exec = shutil.which("java")

        if java_exec is None:
            print("ERROR: Java not available.")
            return

        subprocess.Popen([java_exec, "-jar", str(full_path)], cwd=str(full_path.parent))
        return

    # Windows batch/cmd scripts
    if ext in [".bat", ".cmd"] and os_name == "Windows":
        subprocess.Popen([str(full_path)], cwd=str(full_path.parent), shell=True)
        return

    # macOS .app bundle
    if ext == ".app" and os_name == "Darwin":
        subprocess.Popen(["open", str(full_path)])
        return

    # Shell scripts (.sh)
    if ext == ".sh" and os_name in ["Linux", "Darwin"]:
        os.chmod(full_path, 0o755)
        subprocess.Popen(["/bin/bash", str(full_path)], cwd=str(full_path.parent))
        return

    # Windows .exe
    if os_name == "Windows" and ext == ".exe":
        subprocess.Popen([str(full_path)], cwd=str(full_path.parent), shell=True)
        return

    # Unix executables
    if full_path.is_file() and os.access(full_path, os.X_OK):
        subprocess.Popen([str(full_path)], cwd=str(full_path.parent))
        return

    print("ERROR: Unsupported file type:", ext)
