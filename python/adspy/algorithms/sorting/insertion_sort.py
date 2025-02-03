"""The "Insertion sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Insertion_sort
"""

from collections.abc import Callable, Sequence
from operator import gt, lt
from typing import Any


def _default_key(arg: Any) -> Any:
    return arg


def insertion_sort(
    seq: Sequence,
    key: Callable | None = None,
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

    if key is None:
        key = _default_key
    if not isinstance(key, Callable):
        msg = f"{key} is not callable"
        raise TypeError(msg)

    lst = list(seq)
    if (size := len(lst)) < 2:
        return lst
    op = lt if reverse else gt
    for idx in range(1, size):
        curr = lst[idx]
        jdx = idx - 1
        while jdx > -1 and op(key(lst[jdx]), key(lst[jdx + 1])):
            lst[jdx + 1], lst[jdx] = lst[jdx], lst[jdx + 1]
            jdx -= 1
        lst[jdx + 1] = curr
    return lst
