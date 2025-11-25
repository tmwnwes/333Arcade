from pydantic import BaseModel, ConfigDict
import tomllib
from pathlib import Path
from .config import get_exe_dir

class ProgramMetadata(BaseModel):
    idNum: int
    name: str
    version: str | None = None
    exePath: str
    fullExePath: Path | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def path_fix(self):
        self.fullExePath = get_exe_dir() / self.name / self.exePath
        print("Resolved full path:", self.fullExePath.absolute())
        import os
        print("Files in folder:", os.listdir(self.fullExePath.parent))


def load_metadata(path: Path) -> ProgramMetadata:
    with open(path, "rb") as f:
        data = tomllib.load(f)

    temp = ProgramMetadata(**data)
    temp.path_fix()
    return temp
