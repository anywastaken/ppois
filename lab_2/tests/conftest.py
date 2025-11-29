import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Some modules use absolute imports that expect their directories to be on sys.path.
root_str = str(ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

for subdir in ("manufactoring", "staff", "details", "materials"):
    path = ROOT / subdir
    path_str = str(path)
    if path.exists() and path_str not in sys.path:
        sys.path.insert(0, path_str)


def _ensure_pipx_stub():
    """Provide a minimal stub for pipx.colors used by Driver without pulling the real dependency."""
    if "pipx.colors" in sys.modules:
        return

    pipx_module = types.ModuleType("pipx")
    colors_module = types.ModuleType("pipx.colors")
    colors_module.PRINT_COLOR = None

    sys.modules["pipx"] = pipx_module
    sys.modules["pipx.colors"] = colors_module


_ensure_pipx_stub()
