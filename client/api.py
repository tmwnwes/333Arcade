from __future__ import annotations

import json
import sys
from typing import Any
from pathlib import Path

from .database import (
    init_db,
    add_program,
    list_programs,
    program_exists_by_idnum,
    add_manual_program,
)
from .detection import detect_programs
from .launcher import launch_app


def _ok(data: Any = None) -> dict:
    return {"ok": True, "data": data}


def _err(message: str) -> dict:
    return {"ok": False, "error": message}


def _program_row_to_obj(row) -> dict:
    return {
        "dbId": row[0],
        "idNum": row[1],
        "name": row[2],
        "version": row[3],
        "exePath": row[4],
        "exePathWin": row[5],
        "exePathMac": row[6],
        "fullExePath": row[7],
        "launchVersion": row[8] if len(row) > 8 else None,
    }


def _normalize_optional(s: str | None) -> str | None:
    if s is None:
        return None
    s = s.strip()
    if s == "" or s.lower() in {"none", "null"}:
        return None
    return s


def scan_programs() -> dict:
    conn = init_db()
    added = 0
    skipped = 0

    for meta in detect_programs():
        if not getattr(meta, "fullExePath", None):
            skipped += 1
            continue

        if program_exists_by_idnum(conn, meta.idNum):
            skipped += 1
            continue

        add_program(conn, meta)
        added += 1

    return _ok({"added": added, "skipped": skipped})


def get_programs() -> dict:
    conn = init_db()
    rows = list_programs(conn)
    return _ok([_program_row_to_obj(r) for r in rows])


def launch_program(db_id: int) -> dict:
    conn = init_db()
    rows = list_programs(conn)
    programs = [_program_row_to_obj(r) for r in rows]

    prog = next((p for p in programs if p["dbId"] == db_id), None)
    if prog is None:
        return _err(f"No program with id={db_id}")

    try:
        launch_app(prog["fullExePath"], prog.get("launchVersion"))
        return _ok({"launched": db_id})
    except Exception as e:
        return _err(str(e))


def add_manual(name: str, full_path: str, launch_version: str | None = None) -> dict:
    name = name.strip()
    if not name:
        return _err("Name cannot be empty")

    path = Path(full_path).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()

    if not path.exists():
        return _err(f"Path does not exist: {path}")

    launch_version = _normalize_optional(launch_version)

    conn = init_db()
    new_id = add_manual_program(conn, name=name, full_exe_path=str(path), launch_version=launch_version)
    return _ok({"added": True, "dbId": new_id})


def main():
    """
    Commands:
      python -m client.api scan
      python -m client.api list
      python -m client.api launch <dbId>
      python -m client.api add_manual "<name>" "<fullPath>" [launchVersion]
    """
    if len(sys.argv) < 2:
        print(json.dumps(_err("No command provided")))
        raise SystemExit(2)

    cmd = sys.argv[1]

    try:
        if cmd == "scan":
            out = scan_programs()

        elif cmd == "list":
            out = get_programs()

        elif cmd == "launch":
            if len(sys.argv) < 3:
                out = _err("Missing program id")
            else:
                out = launch_program(int(sys.argv[2]))

        elif cmd == "add_manual":
            if len(sys.argv) < 4:
                out = _err('Usage: add_manual "<name>" "<fullPath>" [launchVersion]')
            else:
                name = sys.argv[2]
                full_path = sys.argv[3]
                launch_version = sys.argv[4] if len(sys.argv) >= 5 else None
                out = add_manual(name, full_path, launch_version)

        else:
            out = _err(f"Unknown command: {cmd}")

        print(json.dumps(out))
    except Exception as e:
        print(json.dumps(_err(f"Unhandled error: {e}")))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
