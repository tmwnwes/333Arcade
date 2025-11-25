from pydantic import BaseModel, ConfigDict
import tomllib
from pathlib import Path
import platform
from .config import get_exe_dir

class ProgramMetadata(BaseModel):
    idNum: int
    name: str
    version: str | None = None

    exePath: str | None = None       # oldVersion
    exePath_win: str | None = None   # Windows
    exePath_mac: str | None = None   # macOS

    fullExePath: Path | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def path_fix(self):
        base = get_exe_dir() / self.name

        # Determine OS
        os_name = platform.system()

        # Fixes null not working in TOML
        if self.exePath == "":
            self.exePath = None
        if self.exePath_win == "":
            self.exePath_win = None
        if self.exePath_mac == "":
            self.exePath_mac = None

        # Pick correct executable path
        if os_name == "Windows":
            exe = self.exePath_win or self.exePath
        elif os_name == "Darwin":  # macOS
            exe = self.exePath_mac or self.exePath
        else:
            exe = self.exePath   # fallback for Linux/testing

        if exe:
            self.fullExePath = base / exe
        else:
            print(f"No valid executable found for {self.name} on {os_name}")
            self.fullExePath = None

        # Debug prints
        print("Resolved full path:", self.fullExePath.absolute() if self.fullExePath else None)
        import os
        if self.fullExePath:
            print("Files in folder:", os.listdir(self.fullExePath.parent))


def load_metadata(path: Path) -> ProgramMetadata:
    with open(path, "rb") as f:
        data = tomllib.load(f)

    temp = ProgramMetadata(**data)
    temp.path_fix()
    return temp
