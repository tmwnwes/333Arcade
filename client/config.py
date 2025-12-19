from pathlib import Path
import tomllib

CONFIG_PATH = (Path(__file__).resolve().parents[1] / "config" / "settings.toml")

def get_metadata_dir() -> Path:
    with open(CONFIG_PATH, "rb") as f:
        data = tomllib.load(f)

    return Path(data["metadata_dir"])

def get_exe_dir() -> Path:
    with open(CONFIG_PATH, "rb") as f:
        data = tomllib.load(f)

    return Path(data["program_dir"])
