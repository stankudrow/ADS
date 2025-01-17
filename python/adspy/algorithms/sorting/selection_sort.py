"""The "Selection sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Selection_sort
"""

from collections.abc import Callable, Sequence
from typing import Any


def selection_sort(
    seq: Sequence,
    key: None | Callable = None,
    *,
    reverse: bool = False,
) -> list:
    """Returns the sorted list.

    Parameters
    ----------
    seq : Sequence
    key : None | Callable, default None
    reverse : bool, default False

    Returns
    -------
    list
    """

    def _default_key(arg) -> Any:
        return arg

    if key is None:
        key = _default_key
    lst = list(seq)
    size = len(lst)
    for idx in range(size):
        imin = idx
        for jdx in range(idx + 1, size):
            if key(lst[jdx]) < key(lst[imin]):
                imin = jdx
        if imin != idx:
            lst[idx], lst[imin] = lst[imin], lst[idx]
    if reverse:
        lst.reverse()
    return lst
