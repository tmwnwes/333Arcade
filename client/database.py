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
            exePath TEXT,
            exePath_win TEXT,
            exePath_mac TEXT,
            fullExePath TEXT,
            launchVersion TEXT
        )"""
    )
    conn.commit()
    return conn

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

        (metadata.idNum, 
         metadata.name, 
         metadata.version, 
         metadata.exePath, 
         metadata.exePath_win, 
         metadata.exePath_mac, 
         str(metadata.fullExePath), 
         metadata.launchVersion)
    )
    conn.commit()

def list_programs(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, idNum, name, version, exePath, exePath_win, exePath_mac, fullExePath, launchVersion FROM programs")
    return cursor.fetchall()