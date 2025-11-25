import subprocess
import os
from pathlib import Path

def launch_app(path):
    full_path = Path(path).absolute()

    if full_path.is_file():
        subprocess.Popen([str(full_path)], shell=True, cwd=str(full_path.parent))
    else:
        print("Executable not found:", full_path)
