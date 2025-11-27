from pathlib import Path
from . import get_project_root   # from __init__

def root() -> Path:
    return get_project_root()

def apps_dir() -> Path:
    return root() / "apps"

def client_dir() -> Path:
    return root() / "client"

def config_dir() -> Path:
    return root() / "config"

def metadata_dir() -> Path:
    return root() / "metadata"

def cmu_graphics_dir() -> Path:
    return root() / "cmu_graphics"
