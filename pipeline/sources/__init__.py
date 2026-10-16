"""Independent sources used to cross-check WID.

Each module exposes `fetch(raw_dir)` (downloads into `<raw_dir>/<name>/`) and
`load(raw_dir) -> dict` (JSON-serializable). The build keys each result by the
module name, so a module's raw folder must carry the same name.
"""
import importlib

NAMES = ["dwa", "insee", "prices", "housing", "rates"]

SOURCES = {}
for _name in NAMES:
    try:
        SOURCES[_name] = importlib.import_module(f"{__name__}.{_name}")
    except ModuleNotFoundError as err:
        if err.name != f"{__name__}.{_name}":
            raise
