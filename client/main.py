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
            launch_app(program[7])                  # FullExePath
            break

if __name__ == "__main__":
    main()
