from pathlib import Path
import sys

plugin_root = Path(__file__).resolve().parent.parent
libs_path = str(plugin_root / "libs")

if libs_path not in sys.path:
    sys.path.insert(0, libs_path)
