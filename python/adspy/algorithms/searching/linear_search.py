"""The "Linear search" algorithm.

References:

- https://en.wikipedia.org/wiki/Linear_search
"""

from collections.abc import Iterable
from typing import Any


def linear_search(it: Iterable, value: Any) -> None | int:
    """Returns the index of the first occurence of the `value`.

    The `it`erable is converted to `tuple` first
    for exhausting possibly given generator objects.
    If None, then the `value` was not found in the `it`erable.

    Parameters
    ----------
    it : Iterable
    value : Any

    Returns
    -------
    None | int
    """

    for idx, item in enumerate(tuple(it)):
        if item == value:
            return idx
    return None
