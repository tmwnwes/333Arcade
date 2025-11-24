from pydantic import BaseModel
from tomllib import toml
from pathlib import Path

class ProgramMetadata(BaseModel):
    id: int
    name: str
    version: str | None = None
    exePath: str

def load_metadata(path:Path) -> ProgramMetadata:
    data = toml.load(path)
    return ProgramMetadata(**data)