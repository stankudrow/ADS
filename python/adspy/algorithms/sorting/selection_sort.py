"""The "Selection sort" algorithm.

References:

- https://en.wikipedia.org/wiki/Selection_sort
"""

from collections.abc import Callable, Sequence
from operator import gt, lt
from typing import Any


def _default_key(arg: Any) -> Any:
    return arg


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

    if key is None:
        key = _default_key
    if not isinstance(key, Callable):
        msg = f"{key} is not callable"
        raise TypeError(msg)

    lst = list(seq)
    if (size := len(lst)) < 2:
        return lst
    op = gt if reverse else lt
    for idx in range(size):
        imin = idx
        for jdx in range(idx + 1, size):
            if op(key(lst[jdx]), key(lst[imin])):
                imin = jdx
        if imin != idx:
            lst[idx], lst[imin] = lst[imin], lst[idx]
    return lst
