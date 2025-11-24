from pathlib import Path
import tomllib

CONFIG_PATH = Path("config/settings.toml")

def get_metadata_dir() -> Path:
    with open(CONFIG_PATH, "rb") as f:
        data = tomllib.load(f)

    return Path(data["metadata_dir"])
