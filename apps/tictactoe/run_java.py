import subprocess
from pathlib import Path
import sys

MAIN_CLASS = "tictactoe.GameMain"

here = Path(__file__).parent

JAVA_HOME = Path(r"C:\Program Files\Java\jdk-21")
javac = JAVA_HOME / "bin" / "javac.exe"
java  = JAVA_HOME / "bin" / "java.exe"

if not javac.exists() or not java.exists():
    print("ERROR: Java not found")
    sys.exit(1)

# Compile ALL java files in this directory
print("Compiling Java...")
java_files = [p.name for p in here.glob("*.java")]

subprocess.check_call(
    [str(javac), "-d", "."] + java_files,
    cwd=here
)

# Run
print("Running Java...")
subprocess.call(
    [str(java), "-cp", ".", MAIN_CLASS],
    cwd=here
)
