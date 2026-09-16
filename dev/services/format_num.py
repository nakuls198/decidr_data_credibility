"""Number helpers for the studio UI and pipeline outputs."""
from __future__ import annotations

from typing import Any

DECIMALS = 5


def full_num(x: Any, fallback: str = "—", decimals: int = DECIMALS) -> str:
    """Format a numeric value to a fixed number of decimal places (default 5)."""
    if x is None:
        return fallback
    try:
        v = float(x)
    except (TypeError, ValueError):
        return str(x)
    if v != v:  # NaN
        return fallback
    return f"{v:.{decimals}f}"


def round_num(x: Any, decimals: int = DECIMALS) -> float | None:
    """Round a numeric value for table/chart display."""
    if x is None:
        return None
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    if v != v:
        return None
    return round(v, decimals)
