from importlib import metadata

try:
    __version__ = metadata.version("prusalink_api")
except Exception:
    __version__ = "0.dev0+unknown"

# flake8: noqa: F405
from .printer import *  # noqa


__all__ = []
__all__.extend(printer.__all__)
