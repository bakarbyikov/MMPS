from itertools import count
from typing import Iterable


def argmax(something: Iterable) -> int:
    return max(zip(something, count()))[-1]


def centrify(string: str, margin_left: int, margin_right: int) -> str:
    return " "*margin_left + string + " "*margin_right
