from importlib.metadata import version

try:
    __version__ = version("stopments")
except Exception:  # pragma: no cover
    __version__ = "unknown"
