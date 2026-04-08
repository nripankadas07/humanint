"""humanint: parse and format human-readable integers.

Public API:
    parse(text)  -> int
    format(value, precision=1) -> str
"""

from .core import parse, format, HumanIntError

__all__ = ["parse", "format", "HumanIntError"]
__version__ = "0.1.0"
