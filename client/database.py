import sqlite3
from pathlib import Path

DB_PATH = Path("client/db/programs.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS programs (
            id INTEGER PRIMARY KEY,
            idNum TEXT,
            name TEXT,
            version TEXT,
            exePath TEXT
        )"""
    )
    conn.commit()
    return conn

def add_program(conn, metadata):
    cursor = conn.cursor()
    cursor.execute(
        """INSERT OR REPLACE INTO programs (idNum, name, version, exePath)
        VALUES (?,?,?,?)""",
        (metadata.idNum, metadata.name, metadata.version, metadata.exePath)
    )
    conn.commit()

def list_programs(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, idNum, name, version, exePath FROM programs")
    return cursor.fetchall()