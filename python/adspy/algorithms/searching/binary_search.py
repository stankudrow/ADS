"""The "Binary search" algorithm.

References:

- https://en.wikipedia.org/wiki/Binary_search
"""

from collections.abc import Iterable
from typing import Any


def binary_search(it: Iterable, value: Any) -> None | int:
    """Returns the index of the first occurence of the `value`.

    The `it`erable must be already sorted,
    no sorting is done under the hood.
    If None, then the `value` was not found in the `it`erable.

    Parameters
    ----------
    it : Iterable
    value : Any

    Returns
    -------
    None | int
    """

    seq = tuple(it)
    left, right = 0, len(seq) - 1
    while left <= right:
        midx = (left + right) // 2
        mid = seq[midx]
        if mid == value:
            return midx
        if mid < value:
            left = midx + 1
        else:
            right = midx - 1
    return None
