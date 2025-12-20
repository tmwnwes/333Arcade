import subprocess
import sys
import shutil
import platform
import os
from pathlib import Path
import webbrowser


def parse_launch_version(version: str | None):
    if version is None:
        return None, None

    if "=" in version:
        runtime, path = version.split("=", 1)
        return runtime.lower(), path.strip()

    return version.lower(), None


def launch_app(path, launch_version=None):
    # Always normalize to string first
    raw = str(path).strip()

    # Steam URL (must be before Path())
    if raw.startswith("steam://"):
        webbrowser.open(raw)
        return

    full_path = Path(raw).expanduser().absolute()
    ext = full_path.suffix.lower()
    os_name = platform.system()

    if not full_path.exists():
        print("ERROR: Path does not exist:", full_path)
        return

    runtime, custom_path = parse_launch_version(launch_version)

    # Compute repo root from this file location
    # client/launcher.py -> repo root is parent of "client"
    repo_root = Path(__file__).resolve().parents[1]
    libraries_path = repo_root / "libraries"

    # Python
    if ext == ".py":
        env = os.environ.copy()

        # Prepend libraries/ to PYTHONPATH (do not overwrite)
        if libraries_path.exists():
            existing = env.get("PYTHONPATH", "")
            if existing:
                env["PYTHONPATH"] = str(libraries_path) + os.pathsep + existing
            else:
                env["PYTHONPATH"] = str(libraries_path)

        if runtime and runtime.startswith("python"):
            python_exec = custom_path or shutil.which(runtime) or sys.executable
            print("Launching Python using:", python_exec)
            subprocess.Popen(
                [python_exec, str(full_path)],
                cwd=str(full_path.parent),
                env=env
            )
            return

        subprocess.Popen(
            [sys.executable, str(full_path)],
            cwd=str(full_path.parent),
            env=env
        )
        return

    # JAR
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

    # Java .class files
    if ext == ".class":
        java_exec = None

        # Allow launchVersion overrides like: "java17" or "java=C:/path/to/java.exe"
        if runtime and runtime.startswith("java"):
            java_exec = custom_path or shutil.which(runtime)

        if java_exec is None:
            java_exec = shutil.which("java")

        if java_exec is None:
            print("ERROR: Java not available.")
            return

        # Run from the folder containing the .class so it’s on the classpath
        class_dir = full_path.parent
        class_name = full_path.stem  # Main.class -> Main

        # Equivalent to: java -cp <dir> Main
        subprocess.Popen([java_exec, "-cp", str(class_dir), class_name], cwd=str(class_dir))
        return

    # Windows batch/cmd
    if ext in [".bat", ".cmd"] and os_name == "Windows":
        subprocess.Popen([str(full_path)], cwd=str(full_path.parent), shell=True)
        return

    # macOS .app bundle
    if ext == ".app" and os_name == "Darwin":
        subprocess.Popen(["open", str(full_path)])
        return

    # Shell scripts
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
