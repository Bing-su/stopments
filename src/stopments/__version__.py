from importlib.metadata import version

try:
    __version__ = version("stopments")
except Exception:
    __version__ = "unknown"
