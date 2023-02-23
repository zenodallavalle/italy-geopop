from decimal import Decimal

from typing import Any


def repr_short(x) -> Any | str:
    if len(str(x)) <= 49:
        return x
    return str(x)[:46] + '...'


def repr_geometry(x) -> str:
    return str(x).split('(', 1)[0][:25]


def repr_floats(x) -> float | Any:
    if isinstance(x, (float, Decimal)):
        return round(float(x), 6)
    return x
