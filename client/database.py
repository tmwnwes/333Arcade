import sqlite3
from pathlib import Path

DB_PATH = Path("client/db/programs.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS programs (
            id INTEGER PRIMARY KEY,
            idNum TEXT,
            name TEXT,
            version TEXT,
            exePath TEXT,
            exePath_win TEXT,
            exePath_mac TEXT,
            fullExePath TEXT,
            launchVersion TEXT
        )"""
    )
    conn.commit()
    return conn


def program_exists_by_idnum(conn, id_num: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM programs WHERE idNum = ? LIMIT 1", (id_num,))
    return cursor.fetchone() is not None


def program_exists_by_full_path(conn, full_exe_path: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM programs WHERE fullExePath = ? LIMIT 1", (full_exe_path,))
    return cursor.fetchone() is not None


def _next_manual_idnum(conn) -> str:
    """
    Manual entries get idNum like: M000001, M000002, ...
    """
    cursor = conn.cursor()
    cursor.execute("SELECT idNum FROM programs WHERE idNum LIKE 'M%' ORDER BY idNum DESC LIMIT 1")
    row = cursor.fetchone()

    if not row or not row[0]:
        return "M000001"

    last = row[0]
    try:
        n = int(last[1:])
    except ValueError:
        # If something weird got into the DB, just restart sequence
        return "M000001"

    return f"M{n + 1:06d}"


def add_manual_program(conn, name: str, full_exe_path: str, launch_version: str | None = None) -> int:
    """
    Insert a manual program entry. Returns the new DB primary key (id).

    Prevent duplicates by fullExePath.
    """
    if program_exists_by_full_path(conn, full_exe_path):
        # Return existing row id to be nice
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM programs WHERE fullExePath = ? LIMIT 1", (full_exe_path,))
        row = cursor.fetchone()
        return int(row[0]) if row else -1

    id_num = _next_manual_idnum(conn)

    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO programs (
            idNum, name, version, exePath, exePath_win, exePath_mac, fullExePath, launchVersion
        ) VALUES (?,?,?,?,?,?,?,?)""",
        (
            id_num,
            name,
            None,   # version (optional later)
            None,   # exePath
            None,   # exePath_win
            None,   # exePath_mac
            full_exe_path,
            launch_version,
        ),
    )
    conn.commit()
    return int(cursor.lastrowid)

def is_manual_db_id(conn, db_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT idNum FROM programs WHERE id = ? LIMIT 1", (db_id,))
    row = cursor.fetchone()
    if not row or not row[0]:
        return False
    return str(row[0]).startswith("M")


def delete_program_by_db_id(conn, db_id: int) -> int:
    """
    Deletes a program row by DB primary key.
    Returns number of rows deleted (0 or 1).
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM programs WHERE id = ?", (db_id,))
    conn.commit()
    return cursor.rowcount


def add_program(conn, metadata):
    cursor = conn.cursor()

    cursor.execute("SELECT idNum FROM programs WHERE idNum = ?", (metadata.idNum,))
    exists = cursor.fetchone()

    if exists:
        print(f"Program with idNum {metadata.idNum} already exists, skipping.")
        return

    cursor.execute(
        """INSERT OR REPLACE INTO programs (
        idNum,
        name,
        version,
        exePath,
        exePath_win,
        exePath_mac,
        fullExePath,
        launchVersion)
        VALUES (?,?,?,?,?,?,?,?)""",
        (
            metadata.idNum,
            metadata.name,
            metadata.version,
            metadata.exePath,
            metadata.exePath_win,
            metadata.exePath_mac,
            str(metadata.fullExePath),
            metadata.launchVersion,
        ),
    )
    conn.commit()


def list_programs(conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, idNum, name, version, exePath, exePath_win, exePath_mac, fullExePath, launchVersion FROM programs"
    )
    return cursor.fetchall()
