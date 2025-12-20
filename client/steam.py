from __future__ import annotations

import os
import platform
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class SteamGame:
    appid: int
    name: str


def _candidate_steam_roots() -> list[Path]:
    sysname = platform.system()

    if sysname == "Windows":
        roots = []
        pf86 = os.environ.get("ProgramFiles(x86)")
        pf = os.environ.get("ProgramFiles")
        lad = os.environ.get("LocalAppData")
        # common Steam installs
        if pf86:
            roots.append(Path(pf86) / "Steam")
        if pf:
            roots.append(Path(pf) / "Steam")
        if lad:
            roots.append(Path(lad) / "Steam")
        return roots

    if sysname == "Darwin":  # macOS
        return [Path.home() / "Library" / "Application Support" / "Steam"]

    # Linux (best-effort)
    return [
        Path.home() / ".steam" / "steam",
        Path.home() / ".local" / "share" / "Steam",
    ]


def _read_text_if_exists(p: Path) -> str | None:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return None


def _extract_library_paths_from_libraryfolders(vdf_text: str) -> list[Path]:
    """
    Steam KeyValues VDF. We only need the library "path" fields.
    Works with both older and newer formats by regexing `"path"  "..."`.
    """
    # matches: "path"    "D:\\SteamLibrary"
    paths = re.findall(r'"path"\s*"([^"]+)"', vdf_text)
    out: list[Path] = []
    for s in paths:
        # libraryfolders.vdf uses double-backslashes sometimes; Path can handle normal strings
        out.append(Path(s))
    return out


def steam_library_paths() -> list[Path]:
    """
    Returns Steam library roots (each contains steamapps/).
    Includes the main Steam install root as a library if it contains steamapps.
    """
    libs: list[Path] = []

    for root in _candidate_steam_roots():
        if not root.exists():
            continue

        # Steam often keeps libraryfolders.vdf under config/
        vdf_candidates = [
            root / "config" / "libraryfolders.vdf",
            root / "steamapps" / "libraryfolders.vdf",
        ]

        # If Steam root itself has steamapps, treat it as a library
        if (root / "steamapps").exists():
            libs.append(root)

        for vdf in vdf_candidates:
            txt = _read_text_if_exists(vdf)
            if not txt:
                continue
            libs.extend(_extract_library_paths_from_libraryfolders(txt))

    # Normalize: keep only libs that actually have steamapps/
    normalized: list[Path] = []
    seen: set[str] = set()
    for lib in libs:
        # some entries point directly at the library root, some at Steam root; steamapps is what we need
        lib = lib.expanduser()
        steamapps = lib / "steamapps"
        if not steamapps.exists():
            continue
        key = str(steamapps.resolve())
        if key in seen:
            continue
        seen.add(key)
        normalized.append(lib)

    return normalized


def _parse_acf_name_and_appid(acf_text: str) -> tuple[int | None, str | None]:
    """
    appmanifest_*.acf is KeyValues. We only need appid + name.
    """
    m_id = re.search(r'"appid"\s*"(\d+)"', acf_text)
    m_name = re.search(r'"name"\s*"([^"]+)"', acf_text)

    appid = int(m_id.group(1)) if m_id else None
    name = m_name.group(1) if m_name else None
    return appid, name


def iter_installed_steam_games() -> Iterable[SteamGame]:
    """
    Enumerates appmanifest_*.acf across all libraries and yields (appid, name).
    """
    for lib in steam_library_paths():
        steamapps = lib / "steamapps"
        for acf in steamapps.glob("appmanifest_*.acf"):
            txt = _read_text_if_exists(acf)
            if not txt:
                continue
            appid, name = _parse_acf_name_and_appid(txt)
            if appid is None or not name:
                continue
            yield SteamGame(appid=appid, name=name)
