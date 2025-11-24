from pydantic import BaseModel
import tomllib
from pathlib import Path

class ProgramMetadata(BaseModel):
    id: int
    name: str
    version: str | None = None
    exePath: str

def load_metadata(path: Path) -> ProgramMetadata:
    with open(path, "rb") as f:
        data = tomllib.load(f)
    return ProgramMetadata(**data)