import subprocess
from pathlib import Path
import os
import sys

MAIN_CLASS = "tictactoe.GameMain"
here = Path(__file__).parent

# Set JAVA_HOME per OS
if sys.platform == "win32":
    os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-21"
elif sys.platform == "darwin":
    os.environ["JAVA_HOME"] = subprocess.check_output(
        ["/usr/libexec/java_home"],
        text=True
    ).strip()

java_home = Path(os.environ["JAVA_HOME"])
javac = java_home / "bin" / ("javac.exe" if os.name == "nt" else "javac")
java  = java_home / "bin" / ("java.exe"  if os.name == "nt" else "java")

print("Compiling Java...")
java_files = [p.name for p in here.glob("*.java")]
subprocess.check_call([str(javac), "-d", "."] + java_files, cwd=here)

print("Running Java...")
subprocess.call([str(java), "-cp", ".", MAIN_CLASS], cwd=here)
