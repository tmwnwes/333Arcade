import subprocess
import os

def launch_app(path:str):
    if os.path.isFile(path):
        subprocess.Popen([path], cwd=os.path.dirname(path))
    else:
        print("Executable not found", path)