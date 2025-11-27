from pydantic import BaseModel, ConfigDict
import tomllib
from pathlib import Path
import platform
from .config import get_exe_dir

class ProgramMetadata(BaseModel):
    idNum: int
    name: str
    version: str | None = None

    exePath: str | None = None       # otherFiles
    exePath_win: str | None = None   # Windows
    exePath_mac: str | None = None   # macOS
    launchVersion: str | None = None
    fullExePath: Path | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def path_fix(self):
        base = get_exe_dir() / self.name
        os_name = platform.system()

        # Normalize empty-string → None for ALL relevant fields
        cleanup_fields = [
            "exePath",
            "exePath_win",
            "exePath_mac",
            "launchVersion"
        ]

        for field in cleanup_fields:
            value = getattr(self, field)
            if value == "":
                setattr(self, field, None)

        # Select the correct executable based on OS
        if os_name == "Windows":
            exe = self.exePath_win or self.exePath
        elif os_name == "Darwin":  # macOS
            exe = self.exePath_mac or self.exePath
        else:
            exe = self.exePath  # fallback for Linux/testing

        # Build full path only if we have something
        if exe:
            self.fullExePath = base / exe
        else:
            print(f"No valid executable found for {self.name} on {os_name}")
            self.fullExePath = None

        # Debug print
        if self.fullExePath:
            print("Resolved full path:", self.fullExePath.absolute())
            import os
            print("Files in folder:", os.listdir(str(self.fullExePath.parent)))

def load_metadata(path: Path) -> ProgramMetadata:
    with open(path, "rb") as f:
        data = tomllib.load(f)

    temp = ProgramMetadata(**data)
    temp.path_fix()
    return temp
