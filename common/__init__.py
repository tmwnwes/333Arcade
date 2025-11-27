# Automatically make the project root importable

from pathlib import Path
import sys

# common/ → project root
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
_ROOT_STR = str(_PROJECT_ROOT)

# Add project root to sys.path so top-level packages work globally
if _ROOT_STR not in sys.path:
    sys.path.insert(0, _ROOT_STR)


def get_project_root():
    return _PROJECT_ROOT
