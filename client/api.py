from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

from .database import (
    init_db,
    add_program,
    list_programs,
    program_exists_by_idnum,
    add_manual_program,
    is_manual_db_id,
    delete_program_by_db_id
)
from .detection import detect_programs
from .launcher import launch_app

API_VERSION = 1


# -------------------------
# hardened IO helpers
# -------------------------

def log(*args: object) -> None:
    """Logs go to stderr so they never corrupt JSON output on stdout."""
    print(*args, file=sys.stderr)


def emit(obj: dict) -> None:
    """Emit exactly one JSON object to stdout."""
    sys.stdout.write(json.dumps(obj, ensure_ascii=False))
    sys.stdout.write("\n")
    sys.stdout.flush()


def ok(data: Any = None, *, meta: dict | None = None) -> dict:
    return {
        "ok": True,
        "data": data,
        "error": None,
        "meta": {"apiVersion": API_VERSION, **(meta or {})},
    }


def fail(code: str, message: str, *, meta: dict | None = None) -> dict:
    return {
        "ok": False,
        "data": None,
        "error": {"code": code, "message": message},
        "meta": {"apiVersion": API_VERSION, **(meta or {})},
    }


def _attach_timing(resp: dict, took_ms: int) -> dict:
    meta = resp.get("meta") or {}
    meta["tookMs"] = took_ms
    resp["meta"] = meta
    return resp


# -------------------------
# serialization helpers
# -------------------------

def _program_row_to_obj(row) -> dict:
    """
    DB row order expected:
    (id, idNum, name, version, exePath, exePath_win, exePath_mac, fullExePath, launchVersion)
    """
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
    # Accept common "no value" inputs
    if s == "" or s.lower() in {"none", "null"}:
        return None
    # Strip surrounding quotes if user pasted a quoted Windows path
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        s = s[1:-1]
    return s


# -------------------------
# API functions
# -------------------------

def scan_programs() -> dict:
    """
    Detect programs from metadata and add them to the DB if missing.
    """
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

    return ok({"added": added, "skipped": skipped})


def get_programs() -> dict:
    """
    Return installed programs as JSON-friendly objects.
    """
    conn = init_db()
    rows = list_programs(conn)
    programs = [_program_row_to_obj(r) for r in rows]
    return ok(programs)


def launch_program(db_id: int) -> dict:
    """
    Launch a program by DB primary key.
    """
    conn = init_db()
    rows = list_programs(conn)
    programs = [_program_row_to_obj(r) for r in rows]

    prog = next((p for p in programs if p["dbId"] == db_id), None)
    if prog is None:
        return fail("NOT_FOUND", f"No program with id={db_id}")

    try:
        launch_app(prog["fullExePath"], prog.get("launchVersion"))
        return ok({"launched": db_id})
    except FileNotFoundError as e:
        return fail("FILE_NOT_FOUND", str(e))
    except Exception as e:
        return fail("LAUNCH_FAILED", str(e))


def add_manual(name: str, full_path: str, launch_version: str | None = None) -> dict:
    """
    Add a manually specified program by absolute (or relative) path.
    This bypasses metadata scanning entirely.
    """
    name = name.strip()
    if not name:
        return fail("INVALID_INPUT", "Name cannot be empty")

    full_path = _normalize_optional(full_path)
    if not full_path:
        return fail("INVALID_INPUT", "Path cannot be empty")

    path = Path(full_path).expanduser()
    # Allow relative paths; store absolute
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()

    if not path.exists():
        return fail("FILE_NOT_FOUND", f"Path does not exist: {path}")

    launch_version = _normalize_optional(launch_version)

    conn = init_db()
    new_db_id = add_manual_program(
        conn=conn,
        name=name,
        full_exe_path=str(path),
        launch_version=launch_version,
    )

    return ok({"added": True, "dbId": new_db_id})

def delete_manual(db_id: int) -> dict:
    conn = init_db()

    # Existence check + manual-only enforcement
    if not is_manual_db_id(conn, db_id):
        return fail("NOT_ALLOWED", f"dbId {db_id} is not a manual entry (or does not exist)")

    deleted = delete_program_by_db_id(conn, db_id)
    if deleted == 0:
        return fail("NOT_FOUND", f"No program with id={db_id}")

    return ok({"deleted": db_id})

# -------------------------
# CLI entry (for Tauri)
# -------------------------

def main() -> None:
    """
    Commands:
      python -m client.api scan
      python -m client.api list
      python -m client.api launch <dbId>
      python -m client.api add_manual "<name>" "<fullPath>" [launchVersion]

    Contract:
      - stdout: JSON only (exactly one line)
      - stderr: logs/debug permitted
    """
    start = time.perf_counter()

    if len(sys.argv) < 2:
        resp = fail("INVALID_COMMAND", "No command provided")
        took_ms = int((time.perf_counter() - start) * 1000)
        emit(_attach_timing(resp, took_ms))
        raise SystemExit(2)

    cmd = sys.argv[1]

    try:
        if cmd == "scan":
            resp = scan_programs()

        elif cmd == "list":
            resp = get_programs()

        elif cmd == "launch":
            if len(sys.argv) < 3:
                resp = fail("INVALID_INPUT", "Missing program id")
            else:
                try:
                    resp = launch_program(int(sys.argv[2]))
                except ValueError:
                    resp = fail("INVALID_INPUT", "Program id must be an integer")

        elif cmd == "add_manual":
            if len(sys.argv) < 4:
                resp = fail("INVALID_INPUT", 'Usage: add_manual "<name>" "<fullPath>" [launchVersion]')
            else:
                name = sys.argv[2]
                full_path = sys.argv[3]
                launch_version = sys.argv[4] if len(sys.argv) >= 5 else None
                resp = add_manual(name, full_path, launch_version)

        elif cmd == "delete_manual":
            if len(sys.argv) < 3:
                resp = fail("INVALID_INPUT", "Missing program id")
            else:
                try:
                    resp = delete_manual(int(sys.argv[2]))
                except ValueError:
                    resp = fail("INVALID_INPUT", "Program id must be an integer")

        else:
            resp = fail("INVALID_COMMAND", f"Unknown command: {cmd}")

    except Exception as e:
        # Never crash without returning JSON.
        log("Unhandled exception in api.py:", repr(e))
        resp = fail("UNHANDLED", str(e))

    took_ms = int((time.perf_counter() - start) * 1000)
    emit(_attach_timing(resp, took_ms))


if __name__ == "__main__":
    main()
