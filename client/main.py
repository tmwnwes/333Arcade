# ---- BOOTSTRAP PROJECT ROOT ----
from pathlib import Path
import sys

# This file lives in project_root/client/main.py
# So project root is one directory up
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROOT_STR = str(PROJECT_ROOT)

if ROOT_STR not in sys.path:
    sys.path.insert(0, ROOT_STR)
# --------------------------------

import common

# Above is experimental code which may be removed in the future
# This may be needed for accessing a higher root

from .database import init_db, add_program, list_programs
from .detection import detect_programs
from .launcher import launch_app

def main():
    conn = init_db()

    print("Detecting programs...")
    for metadata in detect_programs():
        add_program(conn, metadata)
        print(f"Added: {metadata.name}")

    programs = list_programs(conn)
    print("\nInstalled Programs:")
    print("0. Exit")

    for program in programs:
        print(f"{program[0]}. {program[2]}")        # id, name
    choice = int(input("\nEnter program ID to launch: "))
    if choice == 0:
        print("Exiting launcher...")
        return

    for program in programs:
        if program[0] == choice:
            print("Launching", program[2])
            launch_app(program[7], program[8])      # FullExePath, launchVersion
            break

if __name__ == "__main__":
    main()
