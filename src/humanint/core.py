"""Core parsing and formatting for human-readable integers.

Examples
--------
>>> parse("1.5k")
1500
>>> parse("2M")
2000000
>>> format(1500)
'1.5K'
>>> format(2_000_000_000)
'2.0B'
"""

from __future__ import annotations

from typing import Final

# Suffix table: lowercase suffix -> multiplier.
_SUFFIXES: Final[dict[str, int]] = {
    "": 1,
    "k": 1_000,
    "m": 1_000_000,
    "b": 1_000_000_000,
    "t": 1_000_000_000_000,
}

# Ordered list (largest first) used for formatting.
_FORMAT_ORDER: Final[list[tuple[str, int]]] = [
    ("T", 1_000_000_000_000),
    ("B", 1_000_000_000),
    ("M", 1_000_000),
    ("K", 1_000),
]


class HumanIntError(ValueError):
    """Raised when input cannot be parsed as a human-readable integer."""


def _normalize_text(text: str) -> str:
    """Strip whitespace and commas; lowercase. Reject empty input."""
    if not isinstance(text, str):
        raise HumanIntError(f"expected str, got {type(text).__name__}")
    cleaned = text.strip().replace(",", "").replace("_", "")
    if not cleaned:
        raise HumanIntError("input is empty")
    return cleaned


def _split_number_and_suffix(cleaned: str) -> tuple[str, str]:
    """Split a cleaned string into (number_part, suffix_part)."""
    if cleaned[-1].isalpha():
        return cleaned[:-1], cleaned[-1].lower()
    return cleaned, ""


def parse(text: str) -> int:
    """Parse a human-readable number string into an integer.

    Accepts forms like ``"1500"``, ``"1.5k"``, ``"2M"``, ``"-3.2B"``,
    ``"1,000"``, and ``"1_000"``. Suffixes K/M/B/T are case-insensitive.

    Raises:
        HumanIntError: if the input cannot be parsed.
    """
    cleaned = _normalize_text(text)
    number_part, suffix = _split_number_and_suffix(cleaned)
    if suffix not in _SUFFIXES:
        raise HumanIntError(f"unknown suffix: {suffix!r}")
    if not number_part or number_part in ("-", "+"):
        raise HumanIntError(f"missing numeric part in {text!r}")
    try:
        magnitude = float(number_part)
    except ValueError as exc:
        raise HumanIntError(f"invalid numeric part: {number_part!r}") from exc
    result = magnitude * _SUFFIXES[suffix]
    if result != int(result):
        # Allow only when rounding does not lose information.
        raise HumanIntError(
            f"value {text!r} is not an exact integer after suffix expansion"
        )
    return int(result)


def format(value: int, precision: int = 1) -> str:
    """Format an integer as a human-readable string with K/M/B/T suffixes.

    Args:
        value: Integer to format.
        precision: Number of decimal digits to keep (>= 0).

    Raises:
        HumanIntError: if value is not an int or precision is negative.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise HumanIntError(f"expected int, got {type(value).__name__}")
    if not isinstance(precision, int) or precision < 0:
        raise HumanIntError(f"precision must be a non-negative int, got {precision!r}")
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    magnitude = abs(value)
    for suffix, divisor in _FORMAT_ORDER:
        if magnitude >= divisor:
            scaled = magnitude / divisor
            return f"{sign}{scaled:.{precision}f}{suffix}"
    return f"{sign}{magnitude}"
