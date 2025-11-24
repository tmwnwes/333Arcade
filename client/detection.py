from pathlib import Path
from .metadata import load_metadata
from .config import get_metadata_dir

def detect_programs():
    metadata_folder = get_metadata_dir()
    toml_files = metadata_folder.glob("*.toml")

    for file in toml_files:
        yield load_metadata(file)