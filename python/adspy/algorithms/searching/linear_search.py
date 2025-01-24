from collections.abc import Iterable
from typing import Any

def linear_search(it: Iterable, value: Any) -> None | int:
    for idx, item in enumerate(it):
        if item == value:
            return idx
    return None